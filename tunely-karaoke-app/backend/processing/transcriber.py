import whisper_timestamped as whisper
import os

def transcribe_vocals(vocal_track_path):
    """
    Transcribes a vocal audio file to get word-level timestamps.

    Args:
        vocal_track_path (str): The full path to the vocal audio file (e.g., a .wav file).

    Returns:
        list: A list of dictionaries, where each dictionary represents a word and contains:
              {'text': 'word', 'start': 1.23, 'end': 1.45}
              Returns an empty list if transcription fails.
    """
    print(f"Starting transcription for: {vocal_track_path}")

    try:
        # Load the Whisper model. 'base' is a good starting point for speed and accuracy.
        # For higher accuracy with Hindi/Marathi, 'medium' might be better, but it's slower
        # and requires more resources. The model will be downloaded on first use.
        print("  -> Loading Whisper model...")
        audio = whisper.load_audio(vocal_track_path)
        model = whisper.load_model("base", device="cpu") # Use "cuda" if you have a compatible GPU

        # Transcribe the audio, detecting the language automatically.
        # Forcing the language can sometimes improve results if you know it beforehand.
        # e.g., result = whisper.transcribe(model, audio, language="hi")
        print("  -> Performing transcription...")
        result = whisper.transcribe(model, audio, language="hi") # Forcing Hindi for better accuracy

        # --- Data Structuring ---
        # We will re-structure the output to be a simple list of word objects.
        word_timestamps = []
        for segment in result["segments"]:
            for word in segment["words"]:
                word_timestamps.append({
                    'text': word['text'].strip(),
                    'start': word['start'],
                    'end': word['end']
                })
        
        print(f"Transcription complete. Found {len(word_timestamps)} words.")
        return word_timestamps

    except Exception as e:
        print(f"Error during transcription: {e}")
        return []

if __name__ == '__main__':
    # This is for testing the module directly
    # Assumes you have already run the audio_separator and have a vocal track
    test_file = '../outputs/test_song_(Vocals)_UVR-MDX-NET-Inst-HQ-3.wav'
    if os.path.exists(test_file):
        transcription = transcribe_vocals(test_file)
        if transcription:
            print(f"\nTest successful!")
            # Print the first 10 words as an example
            for i, word_data in enumerate(transcription[:10]):
                print(f"  Word {i+1}: Text='{word_data['text']}', Start={word_data['start']:.2f}s, End={word_data['end']:.2f}s")
        else:
            print("\nTest failed.")
    else:
        print(f"Test vocal file not found: {test_file}. Please run audio_separator first.")
