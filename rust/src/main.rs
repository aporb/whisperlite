use std::sync::Arc;
use std::thread;
use std::time::Duration;

use anyhow::Result;
use cpal::traits::{DeviceTrait, HostTrait, StreamTrait};
use crossbeam_channel::{unbounded, Receiver, Sender};
use parking_lot::RwLock;

#[cfg(feature = "ffiwrapper")]
use whisper_rs::{FullParams, SamplingStrategy, WhisperContext};

/// Holds text fragments from transcriber
struct TranscriptBuffer {
    inner: RwLock<Vec<String>>,
}

impl TranscriptBuffer {
    fn new() -> Self {
        Self {
            inner: RwLock::new(Vec::new()),
        }
    }

    fn push(&self, text: String) {
        self.inner.write().push(text);
    }

    fn get_full_text(&self) -> String {
        self.inner.read().join(" ")
    }
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

fn write_transcript_periodically(transcript: Arc<TranscriptBuffer>, path: std::path::PathBuf) {
    thread::spawn(move || loop {
        thread::sleep(Duration::from_secs(5));
        let text = transcript.get_full_text();
        if let Err(e) = std::fs::write(&path, text) {
            eprintln!("failed to write transcript: {}", e);
        }
    });
}

fn main() -> Result<()> {
    let (tx, rx) = unbounded();
    let transcript = Arc::new(TranscriptBuffer::new());

    let downloads = dirs::download_dir().ok_or_else(|| anyhow::anyhow!("No downloads dir"))?;
    let output_path = downloads.join("whisperlite_transcript.txt");
    write_transcript_periodically(transcript.clone(), output_path);

    let _stream = start_audio_capture(tx, 16_000, 1)?;

    #[cfg(feature = "ffiwrapper")]
    {
        let transcript_clone = transcript.clone();
        thread::spawn(move || {
            if let Err(e) = run_transcriber(rx, transcript_clone, "models/ggml-tiny.en.bin") {
                eprintln!("transcriber error: {e}");
            }
        });
    }
    #[cfg(not(feature = "ffiwrapper"))]
    {
        thread::spawn(move || {
            for _ in rx.iter() {
                // no-op transcriber stub
            }
        });
    }

    // Keep alive indefinitely
    loop {
        thread::sleep(Duration::from_secs(1));
    }
}
