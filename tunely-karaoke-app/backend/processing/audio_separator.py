import os
from audio_separator.separator import Separator

def separate_audio(input_audio_path, output_dir):
    """
    Separates an audio file into instrumental and vocal tracks.

    Args:
        input_audio_path (str): The full path to the input audio file.
        output_dir (str): The directory to save the separated audio files.

    Returns:
        tuple: A tuple containing the paths to the instrumental and vocal files.
               e.g., ('path/to/instrumental.wav', 'path/to/vocal.wav')
               Returns (None, None) if separation fails.
    """
    print(f"Starting audio separation for: {input_audio_path}")
    
    try:
        # Initialize the separator with a specific model.
        # 'UVR-MDX-NET-Inst-HQ-3' is a high-quality model for instrumentals.
        separator = Separator(
            output_dir=output_dir,
            model_name='UVR-MDX-NET-Inst-HQ-3',
            output_format='wav' # WAV is best for further processing
        )

        # The library automatically separates into primary and secondary stems.
        # For this model, primary is instrumental, secondary is vocals.
        output_paths = separator.separate(input_audio_path)

        print(f"Separation complete. Output files: {output_paths}")

        # The output_paths list can vary in order. We need to reliably find
        # the instrumental and vocal tracks based on their filenames.
        instrumental_path = None
        vocal_path = None

        for path in output_paths:
            if 'instrumental' in os.path.basename(path).lower():
                instrumental_path = path
            elif 'vocals' in os.path.basename(path).lower():
                vocal_path = path
        
        if not instrumental_path or not vocal_path:
            raise RuntimeError("Could not find instrumental or vocal tracks in the output.")

        return instrumental_path, vocal_path

    except Exception as e:
        print(f"Error during audio separation: {e}")
        return None, None

if __name__ == '__main__':
    # This is for testing the module directly
    # Create a dummy test file or replace with a real audio file path
    test_file = '../uploads/test_song.mp3' # Make sure this file exists
    if os.path.exists(test_file):
        instrumental, vocal = separate_audio(test_file, '../outputs')
        if instrumental and vocal:
            print(f"\nTest successful!")
            print(f"Instrumental track: {instrumental}")
            print(f"Vocal track: {vocal}")
        else:
            print("\nTest failed.")
    else:
        print(f"Test file not found: {test_file}. Please add a song to the uploads folder to test.")

