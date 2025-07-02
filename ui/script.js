// Import Tauri API
const { invoke } = window.__TAURI__.tauri;
const { appWindow } = window.__TAURI__.window;
const { open } = window.__TAURI__.dialog;

// Application state
let isRecording = false;
let transcriptBuffer = '';
let updateInterval = null;

// DOM elements
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const saveBtn = document.getElementById('save-btn');
const clearBtn = document.getElementById('clear-btn');
const statusDot = document.getElementById('status-dot');
const statusText = document.getElementById('status-text');
const transcriptDisplay = document.getElementById('transcript-display');
const modelPathInput = document.getElementById('model-path');
const browseModelBtn = document.getElementById('browse-model-btn');

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('WhisperLite UI initialized');
    
    // Set up event listeners
    setupEventListeners();
    
    // Initialize window properties
    await initializeWindow();
    
    // Load saved model path
    const savedModelPath = localStorage.getItem('whisperlite_model_path');
    if (savedModelPath) {
        modelPathInput.value = savedModelPath;
    }
    
    // Update status
    updateStatus('ready', 'Ready');
});

// Set up all event listeners
function setupEventListeners() {
    startBtn.addEventListener('click', startRecording);
    stopBtn.addEventListener('click', stopRecording);
    saveBtn.addEventListener('click', saveTranscript);
    clearBtn.addEventListener('click', clearTranscript);
    browseModelBtn.addEventListener('click', browseForModel);
    
    // Window event listeners
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

// Initialize window properties
async function initializeWindow() {
    try {
        // Set window to always on top
        await appWindow.setAlwaysOnTop(true);
        
        // Set initial position (top-left corner with some margin)
        await appWindow.setPosition({ x: 50, y: 50 });
        
        console.log('Window initialized successfully');
    } catch (error) {
        console.error('Failed to initialize window:', error);
    }
}

// Browse for Whisper model file
async function browseForModel() {
    try {
        const selected = await open({
            multiple: false,
            filters: [{
                name: 'Whisper Model',
                extensions: ['bin']
            }]
        });
        if (selected) {
            modelPathInput.value = selected;
            localStorage.setItem('whisperlite_model_path', selected);
        }
    } catch (error) {
        console.error('Failed to open file dialog:', error);
    }
}

// Start recording and transcription
async function startRecording() {
    try {
        const modelPath = modelPathInput.value.trim();
        if (!modelPath) {
            showError('Please select a Whisper model file.');
            return;
        }
        
        console.log('Starting recording...');
        updateStatus('processing', 'Starting...');
        
        // Disable start button, enable stop button
        startBtn.disabled = true;
        stopBtn.disabled = false;
        
        // Clear previous transcript if any
        clearTranscriptDisplay();
        
        // Call Tauri backend to start recording, passing the model path
        const result = await invoke('start_transcription', { modelPath: modelPath });
        
        if (result.success) {
            isRecording = true;
            updateStatus('recording', 'Recording');
            
            // Start polling for transcript updates
            startTranscriptPolling();
            
            console.log('Recording started successfully');
        } else {
            throw new Error(result.error || 'Failed to start recording');
        }
        
    } catch (error) {
        console.error('Failed to start recording:', error);
        updateStatus('ready', 'Error: ' + error.message);
        
        // Reset button states
        startBtn.disabled = false;
        stopBtn.disabled = true;
        
        // Show error in transcript area
        showError('Failed to start recording: ' + error.message);
    }
}

// Stop recording and transcription
async function stopRecording() {
    try {
        console.log('Stopping recording...');
        updateStatus('processing', 'Stopping...');
        
        // Call Tauri backend to stop recording
        const result = await invoke('stop_transcription');
        
        isRecording = false;
        
        // Stop polling for updates
        stopTranscriptPolling();
        
        // Reset button states
        startBtn.disabled = false;
        stopBtn.disabled = true;
        
        if (result.success) {
            updateStatus('success', 'Stopped');
            console.log('Recording stopped successfully');
            
            // Get final transcript
            await updateTranscriptDisplay();
        } else {
            throw new Error(result.error || 'Failed to stop recording');
        }
        
    } catch (error) {
        console.error('Failed to stop recording:', error);
        updateStatus('ready', 'Error: ' + error.message);
        showError('Failed to stop recording: ' + error.message);
    }
}

// Save transcript to file
async function saveTranscript() {
    try {
        console.log('Saving transcript...');
        updateStatus('processing', 'Saving...');
        
        const result = await invoke('save_transcript');
        
        if (result.success) {
            updateStatus('success', 'Saved');
            console.log('Transcript saved to:', result.path);
            
            // Show success message briefly
            setTimeout(() => {
                if (!isRecording) {
                    updateStatus('ready', 'Ready');
                } else {
                    updateStatus('recording', 'Recording');
                }
            }, 2000);
        } else {
            throw new Error(result.error || 'Failed to save transcript');
        }
        
    } catch (error) {
        console.error('Failed to save transcript:', error);
        updateStatus('ready', 'Save failed');
        showError('Failed to save transcript: ' + error.message);
    }
}

// Clear transcript display and buffer
async function clearTranscript() {
    try {
        console.log('Clearing transcript...');
        
        const result = await invoke('clear_transcript');
        
        if (result.success) {
            clearTranscriptDisplay();
            transcriptBuffer = '';
            console.log('Transcript cleared');
        } else {
            throw new Error(result.error || 'Failed to clear transcript');
        }
        
    } catch (error) {
        console.error('Failed to clear transcript:', error);
        showError('Failed to clear transcript: ' + error.message);
    }
}

// Start polling for transcript updates
function startTranscriptPolling() {
    if (updateInterval) {
        clearInterval(updateInterval);
    }
    
    updateInterval = setInterval(async () => {
        if (isRecording) {
            await updateTranscriptDisplay();
        }
    }, 1000); // Poll every second
}

// Stop polling for transcript updates
function stopTranscriptPolling() {
    if (updateInterval) {
        clearInterval(updateInterval);
        updateInterval = null;
    }
}

// Update transcript display with latest content
async function updateTranscriptDisplay() {
    try {
        const result = await invoke('get_transcript');
        
        if (result.success && result.transcript !== transcriptBuffer) {
            transcriptBuffer = result.transcript;
            
            if (transcriptBuffer.trim()) {
                let transcriptElement = transcriptDisplay.querySelector('.transcript-text');
                
                if (!transcriptElement) {
                    // If no transcript element exists, remove placeholder and create one
                    transcriptDisplay.innerHTML = ''; // Clear any placeholders
                    transcriptElement = document.createElement('div');
                    transcriptElement.className = 'transcript-text';
                    transcriptDisplay.appendChild(transcriptElement);
                }
                
                // Update the text content
                transcriptElement.textContent = transcriptBuffer;
                
                // Auto-scroll to bottom
                transcriptDisplay.scrollTop = transcriptDisplay.scrollHeight;
            } else {
                // If transcriptBuffer is empty, ensure placeholder is shown
                clearTranscriptDisplay();
            }
        }
        
    } catch (error) {
        console.error('Failed to update transcript:', error);
    }
}

// Clear transcript display
function clearTranscriptDisplay() {
    transcriptDisplay.innerHTML = '<div class="placeholder-text">Click Start to begin transcription...</div>';
}

// Show error message in transcript display
function showError(message) {
    transcriptDisplay.innerHTML = `<div class="placeholder-text" style="color: var(--danger-color);">${message}</div>`;
}

// Update status indicator
function updateStatus(status, text) {
    statusDot.className = `status-dot ${status}`;
    statusText.textContent = text;
}

// Handle keyboard shortcuts
function handleKeyboardShortcuts(event) {
    // Ctrl/Cmd + R: Start/Stop recording
    if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
        event.preventDefault();
        if (isRecording) {
            stopRecording();
        } else {
            startRecording();
        }
    }
    
    // Ctrl/Cmd + S: Save transcript
    if ((event.ctrlKey || event.metaKey) && event.key === 's') {
        event.preventDefault();
        saveTranscript();
    }
    
    // Ctrl/Cmd + D: Clear transcript
    if ((event.ctrlKey || event.metaKey) && event.key === 'd') {
        event.preventDefault();
        clearTranscript();
    }
    
    // Escape: Stop recording
    if (event.key === 'Escape' && isRecording) {
        event.preventDefault();
        stopRecording();
    }
}

// Handle window close event
window.addEventListener('beforeunload', async () => {
    if (isRecording) {
        await stopRecording();
    }
});

// Export functions for debugging
window.WhisperLite = {
    startRecording,
    stopRecording,
    saveTranscript,
    clearTranscript,
    updateTranscriptDisplay,
    isRecording: () => isRecording
};
