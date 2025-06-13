V-O-C: AI Voice Analysis Web Application
Project Overview
V-O-C (Voice-Oriented Computing) is a full-stack web application designed to analyze audio input by transcribing spoken content and extracting sentiment. It provides a straightforward interface for users to either upload existing audio files or record their voice directly through the browser's microphone. The core of the system leverages advanced Hugging Face Transformer models for accurate Speech-to-Text conversion and comprehensive sentiment analysis. The application features a unique, immersive "Matrix"-inspired aesthetic, complete with a dynamic code-rain background effect, offering a visually engaging user experience.

Features
Audio Input Flexibility: Upload .mp3, .wav, .webm, or other common audio formats, or record directly via the browser's microphone.

Speech-to-Text Transcription: Converts spoken audio into text using state-of-the-art AI models.

Sentiment Analysis: Analyzes the transcribed text to determine the overall sentiment (e.g., positive, negative, neutral).

Interactive UI: Displays transcription and sentiment results clearly on the webpage.

Real-time Feedback: Provides status updates during recording and processing.

Matrix-Inspired Design: A custom black and green theme with dynamic falling characters in the background, enhancing the digital aesthetic.

Demo
(Consider adding screenshots or a GIF here once deployed!)

Technologies Used
The project is built with a robust tech stack, combining Python for the powerful backend AI capabilities and modern web technologies for the frontend.

Frontend:

HTML5: Structured content and interactive elements (index.html).

CSS3 (Custom Styling): Implements the "Matrix" black and green theme, including responsive design and visual effects (style.css).

JavaScript: Handles all client-side logic, including:

Web Audio API: For direct microphone access and audio recording.

DOM Manipulation: Dynamically updates the UI with results and status.

Fetch API: Asynchronous communication with the Flask backend.

Canvas API: Renders the dynamic "Matrix rain" background effect (script.js).

Google Fonts: Share Tech Mono for a distinct digital typeface.

Backend:

Python 3.13.5: The core programming language.

Flask: A lightweight web framework for building the API endpoints.

transformers (Hugging Face): Integrates pre-trained ML models for core functionalities:

distil-whisper/distil-small.en: For efficient Automatic Speech Recognition (ASR).

distilbert-base-uncased-finetuned-sst-2-english: For text sentiment analysis.

soundfile: Python library for reading and writing audio files.

librosa: For advanced audio processing, including resampling and channel management, to prepare audio for ML models.

ffmpeg-python: A Pythonic wrapper for FFmpeg, crucial for robust cross-format audio conversion from browser input (WebM) to a format usable by ML models (WAV).

External Dependencies/Tools:

FFmpeg: The essential open-source multimedia framework that provides the underlying audio processing capabilities used by ffmpeg-python and indirectly by soundfile.

Python Virtual Environments (venv): For isolated project dependency management.

Git: For version control.

Prerequisites
Before you can run this project, ensure you have the following installed on your system:

Python 3.13.5 (or a compatible version like 3.11/3.12, as pydub might have issues with 3.13 if you don't use the soundfile/librosa/ffmpeg-python alternative implemented here).

Download from python.org.

pip: Python's package installer (comes with Python).

git: For cloning the repository.

Download from git-scm.com.

FFmpeg: Essential for audio processing.

Download a Windows build (e.g., from gyan.dev/ffmpeg/builds/ or BtbN/FFmpeg-Builds on GitHub).

Crucially, add the bin folder of your FFmpeg installation to your system's PATH environment variables. Verify by opening a new command prompt and running ffmpeg -version.

Installation & Setup
Follow these steps to get the project running on your local machine:

Clone the Repository:
Open your command prompt and navigate to the directory where you want to store your project (e.g., C:\Users\YourUser\Desktop\projects). Then run:

git clone [YOUR_REPOSITORY_URL] # Replace with your actual GitHub repository URL
cd ai-call-analysis # Or whatever your cloned folder is named

Create and Activate a Virtual Environment:
It's highly recommended to use a virtual environment to manage project dependencies.

python -m venv venv
venv\Scripts\activate # On Windows
# source venv/bin/activate # On macOS/Linux

(You should see (venv) at the beginning of your command prompt.)

Install Python Dependencies:
With your virtual environment active, install all required Python packages:

pip install -r requirements.txt

This step will download and install several large libraries (like torch and transformers) and might take several minutes.

(If pip install -r requirements.txt seems to run too quickly or doesn't show progress, ensure your venv is active and try python -m pip install -r requirements.txt.)

Running the Application
Once all dependencies are installed:

Ensure your virtual environment is active ((venv) in your prompt).

Start the Flask backend server:

python app.py

The server will typically start on http://127.0.0.1:5000/.

Open in Browser:
Navigate to http://127.0.0.1:5000/ in your web browser.

Usage
Upload Audio:

Click "Choose File" in the "Upload Audio File" section.

Select an audio file from your computer (e.g., .wav, .mp3).

Click "Analyze Uploaded Audio."

Record Audio:

Click "Start Recording" in the "Record Audio" section. Your browser may ask for microphone permissions (grant them).

Speak into your microphone.

Click "Stop Recording" when finished. You'll see an audio playback control.

Click "Analyze Recorded Audio."

After analysis, the transcribed text and the determined sentiment (e.g., Positive, Negative, Neutral) will be displayed in the "Analysis Results" section.

Customization
Models: You can experiment with different Speech-to-Text or Sentiment Analysis models from the Hugging Face Hub by changing the model parameter in the pipeline calls within app.py. Be aware that larger models require more system resources.

Styling: Modify static/style.css to adjust colors, fonts, and layout to further personalize the "Matrix" theme or create entirely new aesthetics.

Matrix Rain: Adjust font_size, txts (characters), or setInterval timing in static/script.js for the rain effect.

Deployment (Future Considerations)
This application is set up for local development. For production deployment, consider:

Containerization: Using Docker to package the application and all its dependencies for consistent deployment.

WSGI Server: Using a production-grade WSGI server (e.g., Gunicorn for Linux, Waitress for Windows) to serve the Flask application efficiently.

Cloud Platforms: Deploying to platforms like Google Cloud Run, AWS EC2/ECS, or Azure App Service. Google Cloud Run is recommended for its auto-scaling and pay-per-use model, which can be cost-effective for ML-heavy applications with varying traffic.

License
This project is open-source and available under the MIT License. (You may need to create a LICENSE file in your repository with the MIT License text if you choose this.)
