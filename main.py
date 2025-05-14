from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from prompt import SYSTEM_PROMPT
import re

from dotenv import load_dotenv

load_dotenv()

from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment



from dotenv import load_dotenv

load_dotenv()

# Initialize the Kokoro TTS pipeline
pipeline = KPipeline(lang_code="a")

# Assign different voices for speakers
speaker_voices = {
    "JANE": "af_bella",  # Example female voice
    "MIKE": "am_adam"   # Example male voice
}

def generate_podcast(subject: str) -> str:
    """Ask the LLM for a script of a podcast given by two hosts."""
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Here is the topic: {subject[:50]}")
    ]

    llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

    try:
        response = llm.invoke(messages)
    except Exception as e:
        response = f"An error occurred: {e}"
    return response.content

def parse_podcast_script(script: str):
    """
    Parse the podcast script to extract dialogue segments based on speaker labels.
    
    Expects each line to begin with a speaker label like:
      [JANE] Text...
      [MIKE] Text...
    
    Args:
        script (str): The full podcast script.
        
    Returns:
        list of dict: Each dictionary contains 'speaker' and 'text' keys.
    """
    pattern = r'\[([A-Z]+)\]\s*(.*)'  # Correct regex pattern in one line
    segments = []
    for line in script.splitlines():
        match = re.match(pattern, line)
        if match:
            speaker = match.group(1)
            text = match.group(2).strip()
            segments.append({'speaker': speaker, 'text': text})
    return segments

def synthesize_speech(text: str, speaker: str, index: int):
    """Generate speech using Kokoro for each podcast segment."""
    voice = speaker_voices.get(speaker, "af_bella")  # Default fallback voice
    generator = pipeline(text, voice=voice, speed=1, split_pattern=r'\n+')

    for _, _, audio in generator:
        sf.write(f"{index}_{speaker}.wav", audio, 24000)

def merge_audio(segment_files):
    """Merge individual speech segments into a full podcast."""
    podcast = AudioSegment.empty()
    for file in segment_files:
        segment = AudioSegment.from_file(file)
        podcast += segment + AudioSegment.silent(duration=300)  # Add pauses for realism
    podcast.export("final_podcast.mp3", format="mp3")

if __name__ == "__main__":
    # Example topic for generating a podcast script
    subject = "Future of Agents in AI."
    podcast_script = generate_podcast(subject)

    print("Generated Podcast Script:")
    print(podcast_script)

    segments = parse_podcast_script(podcast_script)
    print("Generated Parsed Segments:")
    print(segments)

    # Generate speech files for each speaker
    segment_files = []
    for idx, segment in enumerate(segments):
        filename = f"{idx}_{segment['speaker']}.wav"
        synthesize_speech(segment["text"], segment["speaker"], idx)
        segment_files.append(filename)

    # Merge audio files into a complete podcast
    merge_audio(segment_files)