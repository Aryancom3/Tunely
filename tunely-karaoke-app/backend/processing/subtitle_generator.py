import os
import ass
from datetime import timedelta

def generate_ass_file(transcription_data, output_dir, request_id):
    """
    Generates an .ass subtitle file with word-by-word karaoke effects.

    Args:
        transcription_data (list): The final list of word dictionaries, including speaker info.
        output_dir (str): The directory to save the .ass file.
        request_id (str): The unique ID for this processing request.

    Returns:
        str: The full path to the generated .ass file, or None if it fails.
    """
    print("Starting .ass subtitle file generation...")
    ass_file_path = os.path.join(output_dir, f"{request_id}.ass")

    try:
        doc = ass.Document()

        # --- Define Styles ---
        # This section defines the look of the subtitles. We'll create a base style
        # and then one for each potential speaker with different colors.
        # Colors are in &HBBGGRR format (Blue, Green, Red).
        doc.styles.append(ass.Style(
            name="Default", fontname="Arial", fontsize=28,
            primary_color=ass.Color(r=0xff, g=0xff, b=0xff), # White
            secondary_color=ass.Color(r=0x00, g=0xff, b=0xff), # Yellow for karaoke effect
            outline_color=ass.Color(r=0x00, g=0x00, b=0x00), # Black outline
            back_color=ass.Color(r=0x00, g=0x00, b=0x00, a=0x80), # Semi-transparent black box
            bold=True, alignment=2, # Center alignment
            margin_v=20 # Margin from the bottom
        ))
        
        # You can define more styles for more speakers if needed
        speaker_styles = {
            'SPEAKER_00': 'Speaker1',
            'SPEAKER_01': 'Speaker2',
            # Add more mappings as needed
        }

        doc.styles.append(ass.Style(name="Speaker1", primary_color=ass.Color(r=0x00, g=0xff, b=0xff))) # Yellow
        doc.styles.append(ass.Style(name="Speaker2", primary_color=ass.Color(r=0xff, g=0xcc, b=0xda))) # Light Pink

        # --- Group words into lines ---
        # Logic to group words into reasonable subtitle lines (e.g., max 10 words per line)
        lines = []
        current_line = []
        words_per_line = 8 # Adjust as needed
        
        for i, word_data in enumerate(transcription_data):
            current_line.append(word_data)
            if len(current_line) >= words_per_line or i == len(transcription_data) - 1:
                lines.append(current_line)
                current_line = []

        # --- Create Events (Subtitle Lines) ---
        for line_words in lines:
            if not line_words:
                continue

            start_time = line_words[0]['start']
            end_time = line_words[-1]['end']
            
            # Determine the style for the line based on the first speaker
            first_speaker = line_words[0].get('speaker', 'SPEAKER_00')
            style_name = speaker_styles.get(first_speaker, "Default")

            # Build the text with karaoke tags
            text_parts = []
            for word_data in line_words:
                duration = int((word_data['end'] - word_data['start']) * 100) # Duration in centiseconds
                if duration <= 0: continue # Skip zero-duration words
                text_parts.append(f"{{\\k{duration}}}{word_data['text']}")
            
            line_text = " ".join(text_parts)

            event = ass.Event(
                start=timedelta(seconds=start_time),
                end=timedelta(seconds=end_time),
                text=line_text,
                style=style_name
            )
            doc.events.append(event)

        # --- Save the file ---
        with open(ass_file_path, "w", encoding="utf-8-sig") as f:
            doc.dump(f)

        print(f"Successfully generated subtitle file: {ass_file_path}")
        return ass_file_path

    except Exception as e:
        print(f"Error generating .ass file: {e}")
        return None

if __name__ == '__main__':
    # Dummy data for testing
    dummy_data = [
        {'text': 'This', 'start': 1.0, 'end': 1.5, 'speaker': 'SPEAKER_00'},
        {'text': 'is', 'start': 1.6, 'end': 2.0, 'speaker': 'SPEAKER_00'},
        {'text': 'the', 'start': 2.1, 'end': 2.3, 'speaker': 'SPEAKER_00'},
        {'text': 'first', 'start': 2.4, 'end': 2.9, 'speaker': 'SPEAKER_00'},
        {'text': 'line.', 'start': 3.0, 'end': 3.5, 'speaker': 'SPEAKER_00'},
        {'text': 'And', 'start': 5.0, 'end': 5.3, 'speaker': 'SPEAKER_01'},
        {'text': 'this', 'start': 5.4, 'end': 5.6, 'speaker': 'SPEAKER_01'},
        {'text': 'is', 'start': 5.7, 'end': 5.9, 'speaker': 'SPEAKER_01'},
        {'text': 'the', 'start': 6.0, 'end': 6.2, 'speaker': 'SPEAKER_01'},
        {'text': 'second.', 'start': 6.3, 'end': 6.9, 'speaker': 'SPEAKER_01'},
    ]
    test_output_dir = '../outputs'
    os.makedirs(test_output_dir, exist_ok=True)
    ass_path = generate_ass_file(dummy_data, test_output_dir, 'test_run')
    if ass_path:
        print(f"\nTest successful! File created at: {ass_path}")
    else:
        print("\nTest failed.")
