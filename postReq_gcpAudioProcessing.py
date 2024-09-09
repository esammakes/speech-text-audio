from flask import Flask, request, jsonify, send_from_directory
from google.cloud import speech
import os

app = Flask(__name__)

# Set the path to your service account key file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/emilysam/Desktop/speech-text-audio/arctic-zoo-339006-7b14e2d7ac2d.json'

# Initialize the Google Speech-to-Text client
client = speech.SpeechClient()

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    print("Received request with files:", request.files)  # Debug incoming request
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file'] 
    if file:
        audio_content = file.read()
        audio = speech.RecognitionAudio(content=audio_content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Ensure this matches your audio file
            sample_rate_hertz=16000,  # Ensure this matches your audio file
            language_code="en-US"
        )

        response = client.recognize(config=config, audio=audio)
        print("Google Cloud response:", response)  # Debug the response from Google Cloud
        transcript = response.results[0].alternatives[0].transcript if response.results else ''

        return jsonify({'transcript': transcript})
    else:
        return jsonify({'error': 'No file uploaded'}), 400


# needed to serve the index.html file
@app.route('/')
def send_report():
    return send_from_directory('html','index.html')

@app.route('/audio_capture.js')
def audio():
    return send_from_directory('html','audio_capture.js')

# this was for deployment purposes and is unnecessary for production
if __name__ == '__main__':
    app.run(debug=True)
