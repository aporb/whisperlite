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
const modelSelect = document.getElementById('model-select');
const refreshModelsBtn = document.getElementById('refresh-models-btn');
const downloadModelBtn = document.getElementById('download-model-btn');
const deleteModelBtn = document.getElementById('delete-model-btn');
const downloadProgress = document.getElementById('download-progress');
const progressText = document.getElementById('progress-text');
const modelProgressDiv = document.querySelector('.model-progress');

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    console.log('WhisperLite UI initialized');
    
    setupEventListeners();
    await initializeWindow();
    await loadModels(); // Load models on startup
    
    updateStatus('ready', 'Ready');
});

// Set up all event listeners
function setupEventListeners() {
    startBtn.addEventListener('click', startRecording);
    stopBtn.addEventListener('click', stopRecording);
    saveBtn.addEventListener('click', saveTranscript);
    clearBtn.addEventListener('click', clearTranscript);
    
    modelSelect.addEventListener('change', selectModel);
    refreshModelsBtn.addEventListener('click', loadModels);
    downloadModelBtn.addEventListener('click', downloadModel);
    deleteModelBtn.addEventListener('click', deleteModel);
    
    document.addEventListener('keydown', handleKeyboardShortcuts);
}

async function loadModels() {
    try {
        modelSelect.innerHTML = '<option value="">Loading models...</option>';
        modelSelect.disabled = true;
        refreshModelsBtn.disabled = true;
        downloadModelBtn.disabled = true;
        deleteModelBtn.disabled = true;

        const models = await invoke('list_models');
        modelSelect.innerHTML = '';
        if (models.length === 0) {
            modelSelect.innerHTML = '<option value="">No models found</option>';
        } else {
            models.forEach(model => {
                const option = document.createElement('option');
                option.value = model.path;
                option.textContent = model.name;
                modelSelect.appendChild(option);
            });
            // Select the first model by default or a previously saved one
            const savedModelPath = localStorage.getItem('whisperlite_selected_model');
            if (savedModelPath && models.some(m => m.path === savedModelPath)) {
                modelSelect.value = savedModelPath;
            } else if (models.length > 0) {
                modelSelect.value = models[0].path;
                localStorage.setItem('whisperlite_selected_model', models[0].path);
            }
        }
    } catch (error) {
        console.error('Failed to load models:', error);
        modelSelect.innerHTML = '<option value="">Error loading models</option>';
    } finally {
        modelSelect.disabled = false;
        refreshModelsBtn.disabled = false;
        updateModelActionButtons();
    }
}

function updateModelActionButtons() {
    const selectedModelPath = modelSelect.value;
    const isLocalModel = selectedModelPath && !selectedModelPath.startsWith('http'); // Simple check for local vs remote
    downloadModelBtn.disabled = isLocalModel || !selectedModelPath;
    deleteModelBtn.disabled = !isLocalModel || !selectedModelPath;
}

async function downloadModel() {
    const modelPath = modelSelect.value;
    if (!modelPath) return;

    try {
        downloadModelBtn.disabled = true;
        modelProgressDiv.style.display = 'block';
        updateStatus('processing', 'Downloading...');

        // Placeholder for actual download logic
        // In a real scenario, you'd listen to progress events from Rust
        const result = await invoke('download_model', { modelUrl: modelPath });

        if (result.success) {
            updateStatus('success', 'Download Complete');
            console.log('Model downloaded to:', result.path);
            localStorage.setItem('whisperlite_selected_model', result.path);
            await loadModels(); // Refresh list to show new local model
        } else {
            throw new Error(result.error || 'Failed to download model');
        }
    } catch (error) {
        console.error('Download failed:', error);
        updateStatus('ready', 'Download Failed');
        showError('Model download failed: ' + error.message);
    } finally {
        downloadModelBtn.disabled = false;
        modelProgressDiv.style.display = 'none';
        downloadProgress.value = 0;
        progressText.textContent = '0%';
        updateModelActionButtons();
    }
}

async function deleteModel() {
    const modelPath = modelSelect.value;
    if (!modelPath) return;

    if (!confirm(`Are you sure you want to delete ${modelSelect.options[modelSelect.selectedIndex].textContent}?`)) {
        return;
    }

    try {
        deleteModelBtn.disabled = true;
        updateStatus('processing', 'Deleting...');

        const result = await invoke('delete_model', { modelPath: modelPath });

        if (result.success) {
            updateStatus('success', 'Model Deleted');
            console.log('Model deleted:', modelPath);
            localStorage.removeItem('whisperlite_selected_model');
            await loadModels(); // Refresh list
        } else {
            throw new Error(result.error || 'Failed to delete model');
        }
    } catch (error) {
        console.error('Delete failed:', error);
        updateStatus('ready', 'Delete Failed');
        showError('Model deletion failed: ' + error.message);
    } finally {
        deleteModelBtn.disabled = false;
        updateModelActionButtons();
    }
}

function selectModel() {
    const selectedModelPath = modelSelect.value;
    localStorage.setItem('whisperlite_selected_model', selectedModelPath);
    updateModelActionButtons();
    console.log('Selected model:', selectedModelPath);
}

// Placeholder for Tauri commands (will be implemented in Rust)
// async function list_models() { /* ... */ }
// async function download_model(modelUrl) { /* ... */ }
// async function delete_model(modelPath) { /* ... */ }

// Start recording and transcription
async function startRecording() {
    try {
        const modelPath = modelSelect.value.trim();
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
