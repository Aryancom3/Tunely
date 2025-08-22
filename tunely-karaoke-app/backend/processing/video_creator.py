import subprocess
import os

def create_video(instrumental_track_path, ass_subtitle_path, output_video_path, background_video_path=None):
    """
    Creates the final karaoke video by combining audio, subtitles, and a background.

    Args:
        instrumental_track_path (str): Path to the instrumental audio file.
        ass_subtitle_path (str): Path to the generated .ass subtitle file.
        output_video_path (str): The desired path for the final output video.
        background_video_path (str, optional): Path to a background video. 
                                               If None, a plain black background is used.

    Returns:
        bool: True if video creation was successful, False otherwise.
    """
    print("Starting final video creation...")

    try:
        # --- Build the FFmpeg Command ---
        if background_video_path and os.path.exists(background_video_path):
            # Command with a background video (complex filter)
            # This command is more complex as it needs to loop the background video
            # to match the duration of the audio.
            command = [
                'ffmpeg',
                '-stream_loop', '-1',  # Loop the video input indefinitely
                '-i', background_video_path, # Input 0: Background video
                '-i', instrumental_track_path, # Input 1: Instrumental audio
                '-vf', f"subtitles='{ass_subtitle_path}'", # Video filter to burn subtitles
                '-map', '0:v', # Map video from input 0
                '-map', '1:a', # Map audio from input 1
                '-c:v', 'libx264', # Video codec
                '-preset', 'fast', # Encoding speed preset
                '-crf', '23', # Constant Rate Factor (quality, lower is better)
                '-c:a', 'aac', # Audio codec
                '-b:a', '192k', # Audio bitrate
                '-shortest', # Finish encoding when the shortest input (audio) ends
                '-y', # Overwrite output file if it exists
                output_video_path
            ]
        else:
            # Command for a simple black background
            command = [
                'ffmpeg',
                '-f', 'lavfi', '-i', 'color=c=black:s=1280x720', # Generate a black background
                '-i', instrumental_track_path, # Input audio
                '-vf', f"subtitles='{ass_subtitle_path}'", # Burn subtitles
                '-c:a', 'aac', # Audio codec
                '-b:a', '192k', # Audio bitrate
                '-c:v', 'libx264', # Video codec
                '-preset', 'fast',
                '-crf', '23',
                '-shortest', # Finish when audio ends
                '-y', # Overwrite
                output_video_path
            ]
        
        print(f"  -> Executing FFmpeg command: {' '.join(command)}")

        # --- Run the Command ---
        # We use subprocess.run to execute the command.
        # capture_output=True will store stdout and stderr.
        # text=True decodes them as text.
        result = subprocess.run(command, check=True, capture_output=True, text=True)

        print("  -> FFmpeg stdout:", result.stdout)
        print("  -> FFmpeg stderr:", result.stderr)
        print(f"Successfully created video: {output_video_path}")
        return True

    except FileNotFoundError:
        print("ERROR: ffmpeg command not found. Make sure FFmpeg is installed and in your system's PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print("Error during video creation with FFmpeg.")
        print("FFmpeg stderr:", e.stderr)
        return False
    except Exception as e:
        print(f"An unexpected error occurred in video creation: {e}")
        return False

if __name__ == '__main__':
    # For testing this module directly
    test_instrumental = '../outputs/test_run_(Instrumental)_UVR-MDX-NET-Inst-HQ-3.wav'
    test_ass = '../outputs/test_run.ass'
    test_output = '../outputs/final_karaoke_video.mp4'

    if os.path.exists(test_instrumental) and os.path.exists(test_ass):
        success = create_video(test_instrumental, test_ass, test_output)
        if success:
            print(f"\nTest successful! Video created at: {test_output}")
        else:
            print("\nTest failed.")
    else:
        print("\nTest failed: Make sure instrumental and .ass files exist for the test.")
