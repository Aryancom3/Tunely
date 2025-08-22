import os
from pyannote.audio import Pipeline
import torch

# --- IMPORTANT ---
# Replace "YOUR_HUGGING_FACE_TOKEN" with your actual token.
# It's better to load this from an environment variable in a real application.
HF_TOKEN = "YOUR_HUGGING_FACE_TOKEN" 

def detect_speakers(vocal_track_path, transcription_data):
    """
    Detects different speakers in a vocal track and assigns a speaker ID to each word.

    Args:
        vocal_track_path (str): The path to the vocal audio file.
        transcription_data (list): The list of word timestamp dictionaries from the transcriber.

    Returns:
        list: The updated transcription_data list, with each word dictionary now
              containing a 'speaker' key (e.g., 'SPEAKER_00', 'SPEAKER_01').
    """
    print(f"Starting speaker diarization for: {vocal_track_path}")
    
    if not HF_TOKEN or "hf_bNYQyDkKFVeyThAqbqNLsUCTnSxMqOEWovTOKEN" in HF_TOKEN:
        print("ERROR: Hugging Face token is not set. Please add your token to speaker_diarizer.py")
        # Add speaker 'UNKNOWN' to all words and return
        for word in transcription_data:
            word['speaker'] = 'UNKNOWN'
        return transcription_data

    try:
        # 1. --- Load the pre-trained diarization pipeline ---
        print("  -> Loading speaker diarization pipeline...")
        device = "cuda" if torch.cuda.is_available() else "cpu"
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            use_auth_token=HF_TOKEN
        ).to(torch.device(device))

        # 2. --- Apply the pipeline to the audio file ---
        print("  -> Applying pipeline to audio...")
        diarization = pipeline(vocal_track_path)

        # 3. --- Map words to speakers ---
        print("  -> Mapping words to speakers...")
        for word in transcription_data:
            word_center = word['start'] + (word['end'] - word['start']) / 2
            
            # Find which speaker was active at the center of the word's duration
            try:
                speaker = diarization.get_labels(word_center)[0]
                word['speaker'] = speaker
            except IndexError:
                # If no speaker is found at that exact moment (e.g., silence)
                word['speaker'] = 'UNKNOWN'
        
        print("Speaker diarization complete.")
        return transcription_data

    except Exception as e:
        print(f"Error during speaker diarization: {e}")
        # In case of an error, we'll still return the data without speaker info
        for word in transcription_data:
            word['speaker'] = 'ERROR'
        return transcription_data

if __name__ == '__main__':
    # This is for testing the module directly
    test_file = '../outputs/test_song_(Vocals)_UVR-MDX-NET-Inst-HQ-3.wav'
    # Dummy transcription data for testing
    dummy_data = [
        {'text': 'Hello', 'start': 1.0, 'end': 1.5},
        {'text': 'world', 'start': 1.6, 'end': 2.0},
        {'text': 'this', 'start': 5.0, 'end': 5.3},
        {'text': 'is', 'start': 5.4, 'end': 5.6},
        {'text': 'a', 'start': 5.7, 'end': 5.8},
        {'text': 'test', 'start': 5.9, 'end': 6.5},
    ]
    if os.path.exists(test_file):
        data_with_speakers = detect_speakers(test_file, dummy_data)
        if data_with_speakers:
            print(f"\nTest successful!")
            for word_data in data_with_speakers:
                print(f"  Word='{word_data['text']}', Speaker='{word_data.get('speaker', 'N/A')}'")
        else:
            print("\nTest failed.")
    else:
        print(f"Test vocal file not found: {test_file}. Please run audio_separator first.")
