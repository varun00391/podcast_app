from utils import generate_podcast,parse_podcast_script,synthesize_speech,merge_audio
from prompt import SYSTEM_PROMPT


subject = "Nuclear capabilitites of India"

podcast_script = generate_podcast(subject)
segments = parse_podcast_script(podcast_script)

# Generate speech files for each speaker
segment_files = []
for idx, segment in enumerate(segments):
    filename = f"{idx}_{segment['speaker']}.wav"
    synthesize_speech(segment["text"], segment["speaker"], idx)
    segment_files.append(filename)

# Merge audio files into a complete podcast
merge_audio(segment_files)
