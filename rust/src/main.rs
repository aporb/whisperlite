use std::sync::Arc;
use std::thread;
use std::time::Duration;
use std::process::{Child, Command, Stdio};
use std::io::{BufReader, BufRead, Write};

use anyhow::Result;
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use crossbeam_channel::{unbounded, Receiver, Sender};
use parking_lot::RwLock;
use tauri::{State, Manager};

#[cfg(feature = "ffiwrapper")]
use whisper_rs::{FullParams, SamplingStrategy, WhisperContext};

/// Holds text fragments from transcriber
pub struct TranscriptBuffer {
    inner: RwLock<Vec<String>>,
}

impl TranscriptBuffer {
    pub fn new() -> Self {
        Self {
            inner: RwLock::new(Vec::new()),
        }
    }

    pub fn push(&self, text: String) {
        self.inner.write().push(text);
    }

    pub fn get_full_text(&self) -> String {
        self.inner.read().join(" ")
    }

    pub fn clear(&self) {
        self.inner.write().clear();
    }
}

pub struct AppState {
    transcript_buffer: Arc<TranscriptBuffer>,
    is_recording: Arc<RwLock<bool>>,
    audio_sender: Arc<RwLock<Option<Sender<Vec<i16>>>>>, // Channel to send audio chunks
    stream_handle: Arc<RwLock<Option<cpal::Stream>>>,
    python_process: Arc<RwLock<Option<Child>>>,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            transcript_buffer: Arc::new(TranscriptBuffer::new()),
            is_recording: Arc::new(RwLock::new(false)),
            audio_sender: Arc::new(RwLock::new(None)),
            stream_handle: Arc::new(RwLock::new(None)),
            python_process: Arc::new(RwLock::new(None)),
        }
    }
}

#[derive(serde::Serialize)]
pub struct CommandResponse {
    success: bool,
    message: Option<String>,
    transcript: Option<String>,
    path: Option<String>,
    error: Option<String>,
}



/// Capture audio from microphone and send raw samples to a channel
fn start_audio_capture(tx: Sender<Vec<i16>>, sample_rate: u32, channels: u16) -> Result<cpal::Stream> {
    let host = cpal::default_host();
    let device = host
        .default_input_device()
        .ok_or_else(|| anyhow::anyhow!("No input device available"))?;
    let config = device.default_input_config()?;

    let sr = sample_rate;
    let channels = channels as usize;
    let err_fn = |err| eprintln!("stream error: {}", err);

    let stream_config = cpal::StreamConfig {
        channels: channels as u16,
        sample_rate: cpal::SampleRate(sr),
        buffer_size: cpal::BufferSize::Default,
    };

    let mut sample_buffer = Vec::<i16>::new();
    let frames_per_chunk = (sr as f32 * 1.5) as usize * channels;
    let tx_clone = tx.clone();

    let stream = device.build_input_stream(
        &stream_config,
        move |data: &[i16], _| {
            sample_buffer.extend_from_slice(data);
            while sample_buffer.len() >= frames_per_chunk {
                let chunk: Vec<i16> = sample_buffer.drain(..frames_per_chunk).collect();
                if tx_clone.send(chunk).is_err() {
                    return;
                }
            }
        },
        err_fn,
        None,
    )?;
    stream.play()?;
    Ok(stream)
}

#[cfg(feature = "ffiwrapper")]
fn run_transcriber(rx: Receiver<Vec<i16>>, transcript: Arc<TranscriptBuffer>, model_path: &str) -> Result<()> {
    let ctx = WhisperContext::new(model_path)?;
    let mut params = FullParams::new(SamplingStrategy::Greedy { best_of: 1 });
    params.set_language(Some("en"));

    for audio in rx.iter() {
        let mut audio_f32: Vec<f32> = audio.iter().map(|s| *s as f32 / i16::MAX as f32).collect();
        let mut state = ctx.create_state()?;
        state.full(params, &mut audio_f32)?;
        let num_segments = state.full_n_segments();
        let mut text = String::new();
        for i in 0..num_segments {
            text.push_str(state.full_get_segment_text(i));
        }
        transcript.push(text.trim().to_string());
    }
    Ok(())
}

#[tauri::command]
async fn start_transcription(model_path: String, state: State<'_, AppState>) -> Result<CommandResponse, String> {
    let mut is_recording = state.is_recording.write();
    if *is_recording {
        return Ok(CommandResponse { success: false, message: Some("Already recording".into()), transcript: None, path: None, error: None });
    }

    let (tx, rx) = unbounded();
    *state.audio_sender.write() = Some(tx);

    let transcript_clone = state.transcript_buffer.clone();
    let model_path_clone = model_path.clone();

    // Spawn Python subprocess
    let python_process = Command::new("python3")
        .arg("src/main.py")
        .arg("--model")
        .arg(model_path_clone)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .spawn();

    match python_process {
        Ok(mut child) => {
            let stdin = child.stdin.take().expect("Failed to open stdin");
            let stdout = child.stdout.take().expect("Failed to open stdout");

            // Thread to send audio to Python
            let audio_rx = rx.clone();
            thread::spawn(move || {
                for chunk in audio_rx.iter() {
                    // Convert i16 to bytes and send to Python stdin
                    let bytes: Vec<u8> = chunk.iter().flat_map(|&s| s.to_le_bytes().to_vec()).collect();
                    if let Err(e) = std::io::Write::write_all(&mut stdin.lock().unwrap(), &bytes) {
                        eprintln!("Failed to write to python stdin: {}", e);
                        break;
                    }
                }
            });

            // Thread to read transcript from Python
            let transcript_buffer_clone = transcript_clone.clone();
            thread::spawn(move || {
                let reader = BufReader::new(stdout);
                for line in reader.lines() {
                    match line {
                        Ok(text) => {
                            transcript_buffer_clone.push(text);
                        },
                        Err(e) => {
                            eprintln!("Failed to read from python stdout: {}", e);
                            break;
                        }
                    }
                }
            });

            *state.python_process.write().take() = Some(child);

            // Start audio capture
            match start_audio_capture(tx, 16_000, 1) {
                Ok(stream) => {
                    *state.stream_handle.write().take() = Some(stream);
                    *is_recording = true;
                    Ok(CommandResponse { success: true, message: Some("Recording started".into()), transcript: None, path: None, error: None })
                },
                Err(e) => {
                    eprintln!("Failed to start audio capture: {}", e);
                    // Kill python process if audio capture fails
                    if let Some(mut p) = state.python_process.write().take() {
                        let _ = p.kill();
                    }
                    Err(e.to_string())
                }
            }
        },
        Err(e) => {
            eprintln!("Failed to spawn python process: {}", e);
            Err(format!("Failed to start transcription: {}", e))
        }
    }
}

#[tauri::command]
async fn stop_transcription(state: State<'_, AppState>) -> Result<CommandResponse, String> {
    let mut is_recording = state.is_recording.write();
    if !*is_recording {
        return Ok(CommandResponse { success: false, message: Some("Not recording".into()), transcript: None, path: None, error: None });
    }

    // Stop audio stream
    if let Some(stream) = state.stream_handle.write().take() {
        drop(stream);
    }

    // Kill Python process
    if let Some(mut p) = state.python_process.write().take() {
        let _ = p.kill();
    }

    *is_recording = false;
    Ok(CommandResponse { success: true, message: Some("Recording stopped".into()), transcript: None, path: None, error: None })
}

#[tauri::command]
async fn get_transcript(state: State<'_, AppState>) -> Result<CommandResponse, String> {
    let transcript = state.transcript_buffer.get_full_text();
    Ok(CommandResponse { success: true, message: None, transcript: Some(transcript), path: None, error: None })
}

#[tauri::command]
async fn save_transcript(state: State<'_, AppState>) -> Result<CommandResponse, String> {
    let transcript = state.transcript_buffer.get_full_text();
    let downloads = dirs::download_dir().ok_or_else(|| "No downloads directory found".to_string())?;
    let filename = format!("whisperlite_transcript_{}.txt", chrono::Local::now().format("%Y%m%d_%H%M%S"));
    let path = downloads.join(filename);

    match std::fs::write(&path, transcript) {
        Ok(_) => Ok(CommandResponse { success: true, message: Some("Transcript saved".into()), transcript: None, path: Some(path.to_string_lossy().into_owned()), error: None }),
        Err(e) => Err(format!("Failed to save transcript: {}", e)),
    }
}

#[tauri::command]
async fn clear_transcript(state: State<'_, AppState>) -> Result<CommandResponse, String> {
    state.transcript_buffer.clear();
    Ok(CommandResponse { success: true, message: Some("Transcript cleared".into()), transcript: None, path: None, error: None })
}

fn main() -> Result<()> {
    tauri::Builder::default()
        .manage(AppState::default())
        .invoke_handler(tauri::generate_handler![
            start_transcription,
            stop_transcription,
            get_transcript,
            save_transcript,
            clear_transcript
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");

    Ok(())
}