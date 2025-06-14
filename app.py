# app.py
from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import os
import io
import soundfile as sf
import librosa # Used for resampling and channel conversion
import ffmpeg # THIS IS THE NEW IMPORT FOR FFMPEG-PYTHON
import uuid # For unique temporary filenames

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Hugging Face Pipelines
# Speech-to-Text (e.g., 'distil-whisper/distil-small.en')
# For better performance, consider 'openai/whisper-small' or 'openai/whisper-base'
# The model chosen will depend on your system's resources and desired accuracy.
try:
    transcriber = pipeline("automatic-speech-recognition", model="distil-whisper/distil-small.en", device=0) # device=0 for GPU, -1 for CPU
    print("Speech-to-Text model loaded successfully.")
except Exception as e:
    print(f"Error loading ASR model, falling back to CPU or different model: {e}")
    transcriber = pipeline("automatic-speech-recognition", model="distil-whisper/distil-small.en", device=-1)

# Sentiment Analysis (e.g., 'distilbert-base-uncased-finetuned-sst-2-english')
try:
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=0) # device=0 for GPU, -1 for CPU
    print("Sentiment Analysis model loaded successfully.")
except Exception as e:
    print(f"Error loading Sentiment Analysis model, falling back to CPU: {e}")
    sentiment_analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english", device=-1)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_audio', methods=['POST'])
def analyze_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({"error": "No selected audio file"}), 400

    # Generate unique temporary file paths for the input and output audio
    unique_id = str(uuid.uuid4())
    input_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_input.webm")
    output_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_output.wav")

    try:
        # Step 1: Save the incoming audio (which is WebM from the browser) to a temporary file
        audio_file.save(input_audio_path)
        print(f"Saved input audio to {input_audio_path}")

        # Step 2: Use ffmpeg-python to convert the input WebM file to a standard WAV file
        # This is the crucial step for robust format recognition
        (
            ffmpeg
            .input(input_audio_path)
            .output(output_audio_path, acodec='pcm_s16le', ac=1, ar='16k') # Output WAV, PCM 16-bit, mono, 16kHz
            .overwrite_output() # Overwrite if file exists
            .run(capture_stdout=True, capture_stderr=True)
        )
        print(f"Converted audio from {input_audio_path} to {output_audio_path} using FFmpeg.")

        # Step 3: Now, use soundfile to read the perfectly standard WAV file
        data, original_sr = sf.read(output_audio_path)

        # The ffmpeg-python step should have already ensured 16kHz mono.
        # These librosa checks are largely redundant now but can act as safeguards.
        target_sr = 16000
        if data.ndim > 1:
            data = librosa.to_mono(data.T)
            print(f"Safeguard: Converted audio to mono. Shape: {data.shape}")

        if original_sr != target_sr:
            print(f"Safeguard: Resampling audio from {original_sr} Hz to {target_sr} Hz. Original shape: {data.shape}")
            data = librosa.resample(y=data, orig_sr=original_sr, target_sr=target_sr)
            print(f"Safeguard: Resampled audio shape: {data.shape}")

        # Step 4: Perform Speech-to-Text on the converted WAV file
        transcription_result = transcriber(output_audio_path)
        transcription = transcription_result['text']

        # Step 5: Perform Sentiment Analysis
        sentiment_result = sentiment_analyzer(transcription)
        sentiment_label = sentiment_result[0]['label']
        sentiment_score = sentiment_result[0]['score']

        return jsonify({
            "transcription": transcription,
            "sentiment": {
                "label": sentiment_label,
                "score": round(sentiment_score, 4)
            }
        })

    except ffmpeg.Error as e:
        # Log FFmpeg-specific errors for debugging
        print(f"FFmpeg conversion failed. STDOUT: {e.stdout.decode()} STDERR: {e.stderr.decode()}")
        return jsonify({"error": f"Audio conversion failed: {e.stderr.decode()}"}), 500
    except Exception as e:
        # Catch any other unexpected errors during processing
        print(f"An unexpected error occurred during audio processing: {e}")
        return jsonify({"error": f"Failed to process audio: {str(e)}"}), 500
    finally:
        # Ensure temporary files are cleaned up, regardless of success or failure
        if os.path.exists(input_audio_path):
            os.remove(input_audio_path)
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
