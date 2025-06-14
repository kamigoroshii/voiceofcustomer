document.addEventListener('DOMContentLoaded', () => {
    // Existing UI elements
    const audioUpload = document.getElementById('audioUpload');
    const uploadButton = document.getElementById('uploadButton');
    const recordButton = document.getElementById('recordButton');
    const stopButton = document.getElementById('stopButton');
    const analyzeRecordedButton = document.getElementById('analyzeRecordedButton');
    const recordingStatus = document.getElementById('recordingStatus');
    const audioPlayback = document.getElementById('audioPlayback');
    const loadingSpinner = document.getElementById('loading');
    const errorMessage = document.getElementById('error');
    const resultsSection = document.getElementById('resultsSection');
    const transcriptionResult = document.getElementById('transcriptionResult');
    const sentimentResult = document.getElementById('sentimentResult');
    // Removed containerElement as it's only needed for Matrix rain
    
    let mediaRecorder;
    let audioChunks = [];
    let recordedBlob;

    // --- Utility Functions ---
    function showLoading() {
        loadingSpinner.style.display = 'block';
        errorMessage.style.display = 'none';
        resultsSection.style.display = 'none';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        hideLoading();
        resultsSection.style.display = 'none';
    }

    function showResults(transcription, sentiment) {
        transcriptionResult.textContent = transcription;
        sentimentResult.textContent = `${sentiment.label} (Score: ${sentiment.score})`;
        resultsSection.style.display = 'block';
        hideLoading();
        errorMessage.style.display = 'none';
    }

    function resetUI() {
        audioPlayback.style.display = 'none';
        audioPlayback.removeAttribute('src');
        recordingStatus.textContent = '';
        transcriptionResult.textContent = '';
        sentimentResult.textContent = '';
        resultsSection.style.display = 'none';
        errorMessage.style.display = 'none';
    }

    // --- Audio Upload Logic ---
    uploadButton.addEventListener('click', async () => {
        const file = audioUpload.files[0];
        if (!file) {
            showError('Please select an audio file to upload.');
            return;
        }

        resetUI();
        showLoading();

        const formData = new FormData();
        formData.append('audio', file);

        try {
            const response = await fetch('/analyze_audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error.');
            }

            const data = await response.json();
            showResults(data.transcription, data.sentiment);

        } catch (error) {
            console.error('Error uploading audio:', error);
            showError(`Analysis failed: ${error.message}`);
        }
    });

    // --- Audio Recording Logic ---
    recordButton.addEventListener('click', async () => {
        resetUI();
        audioChunks = [];
        recordedBlob = null;

        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' }); 

            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = () => {
                recordedBlob = new Blob(audioChunks, { type: 'audio/webm' }); 
                console.log('Recorded Blob type:', recordedBlob.type);

                const audioURL = URL.createObjectURL(recordedBlob);
                audioPlayback.src = audioURL;
                audioPlayback.style.display = 'block';
                recordingStatus.textContent = 'Recording stopped. Ready for analysis.';
                analyzeRecordedButton.disabled = false;
                recordButton.disabled = false;
                stopButton.disabled = true;
            };

            mediaRecorder.start();
            recordingStatus.textContent = 'Recording...';
            recordButton.disabled = true;
            stopButton.disabled = false;
            analyzeRecordedButton.disabled = true;

        } catch (err) {
            console.error('Error accessing microphone:', err);
            showError('Failed to access microphone. Please ensure permissions are granted.');
            recordButton.disabled = false;
            stopButton.disabled = true;
            analyzeRecordedButton.disabled = true;
        }
    });

    stopButton.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state === 'recording') {
            mediaRecorder.stop();
            mediaRecorder.stream.getTracks().forEach(track => track.stop());
        }
    });

    analyzeRecordedButton.addEventListener('click', async () => {
        if (!recordedBlob) {
            showError('No recorded audio found. Please record first.');
            return;
        }

        showLoading();

        const formData = new FormData();
        formData.append('audio', recordedBlob, 'recorded_audio.webm'); 

        try {
            const response = await fetch('/analyze_audio', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error.');
            }

            const data = await response.json();
            showResults(data.transcription, data.sentiment);

        } catch (error) {
            console.error('Error analyzing recorded audio:', error);
            showError(`Analysis failed: ${error.message}`);
        } finally {
            analyzeRecordedButton.disabled = true;
        }
    });

    // Removed all Matrix Rain Effect Logic here
}); // End of DOMContentLoaded
