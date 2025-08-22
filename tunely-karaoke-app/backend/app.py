import os
from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import uuid # To generate unique filenames

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# --- Helper Functions ---
def allowed_file(filename):
    """Checks if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folders():
    """Creates necessary folders if they don't exist."""
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# --- Main API Endpoint ---
@app.route('/api/process-karaoke', methods=['POST'])
def process_karaoke():
    """
    The main endpoint to handle audio upload and karaoke video generation.
    """
    # 1. --- Handle File Upload ---
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    if file and allowed_file(file.filename):
        # Generate a unique ID for this request to prevent filename conflicts
        request_id = str(uuid.uuid4())
        original_filename = secure_filename(file.filename)
        input_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{request_id}_{original_filename}")
        file.save(input_audio_path)
        
        print(f"File saved to: {input_audio_path}")

        try:
            # --- PROCESSING PIPELINE ---
            
            # 2. --- Audio Separation (Vocals & Instrumental) ---
            # TODO: Implement logic from processing/audio_separator.py
            # This function should take `input_audio_path` and return two paths:
            # `vocal_track_path` and `instrumental_track_path`
            print("Step 2: Separating audio...")
            # instrumental_track_path, vocal_track_path = separate_audio(input_audio_path)
            
            # 3. --- Transcription (Word-level Timestamps) ---
            # TODO: Implement logic from processing/transcriber.py
            # This function should take `vocal_track_path` and return a data structure
            # with words, start times, and end times.
            print("Step 3: Transcribing vocals...")
            # transcription_data = transcribe_vocals(vocal_track_path)

            # 4. --- Speaker Diarization (Optional but required for color-coding) ---
            # TODO: Implement speaker detection on `vocal_track_path`
            # This would update `transcription_data` with speaker labels (e.g., 'SPEAKER_00', 'SPEAKER_01')
            print("Step 4: Detecting speakers...")
            # transcription_data_with_speakers = detect_speakers(vocal_track_path, transcription_data)

            # 5. --- Generate .ass Subtitle File ---
            # TODO: Implement logic from processing/subtitle_generator.py
            # This function takes the final transcription data and creates a .ass file.
            print("Step 5: Generating karaoke subtitles...")
            # ass_subtitle_path = generate_ass_file(transcription_data_with_speakers, request_id)

            # 6. --- Burn Subtitles into Video using FFmpeg ---
            # TODO: Implement logic from processing/video_creator.py
            # This function combines a background, the instrumental track, and the .ass subtitles.
            print("Step 6: Creating final video...")
            output_video_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{request_id}.mp4")
            # create_video(instrumental_track_path, ass_subtitle_path, output_video_path)
            
            # --- For Demo Purposes: We'll just return a success message for now ---
            # In the real implementation, you would return the path to the video
            return jsonify({
                "message": "Processing complete!",
                "video_url": f"/outputs/{request_id}.mp4" # URL the frontend can use
            }), 200

        except Exception as e:
            # Basic error handling
            print(f"An error occurred: {e}")
            return jsonify({"error": "Failed to process the audio file. Please try again."}), 500
    else:
        return jsonify({"error": "File type not allowed"}), 400

@app.route('/outputs/<filename>')
def get_output_video(filename):
    """Serves the generated video file to the user."""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

if __name__ == '__main__':
    create_folders()
    app.run(debug=True, port=5000) # Runs on http://127.0.0.1:5000
