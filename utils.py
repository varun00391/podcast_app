from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from prompt import SYSTEM_PROMPT
import re, os

from dotenv import load_dotenv

from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment


load_dotenv()


class PodCastGenerator():
    def __init__(self,lang_code = 'a'):
    
        """Initialize the Kokoro TTS pipeline and speaker voices."""
        self.pipeline = KPipeline(lang_code=lang_code)
        self.speaker_voices = {
            "JANE": "af_bella",  # Example female voice
            "MIKE": "am_adam"    # Example male voice
        }

    def generate_podcast_script(self,subject: str) -> str:
        """Ask the LLM for a script of a podcast given by two hosts."""
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Here is the topic: {subject[:200]}")
        ]

        llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.7,max_tokens=4000)

        try:
            response = llm.invoke(messages)
        except Exception as e:
            response = f"An error occurred: {e}"
        return response.content

    def parse_podcast_script(self,script: str):
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

    def synthesize_speech(self, text: str, speaker: str, index: int):
        """Generate speech using Kokoro for each podcast segment and yield file names."""
        voice = self.speaker_voices.get(speaker, "af_bella")  # Default fallback voice
        generator = self.pipeline(text, voice=voice, speed=1, split_pattern=r'\n+')

        for _, _, audio in generator:
            filename = f"{index}_{speaker}.wav"
            sf.write(filename, audio, 24000)
            yield filename


    def merge_audio(self,segment_files):
        """Merge individual speech segments into a full podcast and clean up temporary files."""
        podcast = AudioSegment.empty()
        
        for file in segment_files:
            segment = AudioSegment.from_file(file)
            podcast += segment + AudioSegment.silent(duration=300)  # Add pauses for realism
        
        final_output = "final_podcast.mp3"
        podcast.export(final_output, format="mp3")
        
        # Ensure final podcast exists before deleting temporary files
        if os.path.exists(final_output):
            for file in segment_files:
                os.remove(file)
        
        return final_output
    
    def create_podcast(self, subject: str):
        """Full pipeline from script generation to final podcast output."""
        script = self.generate_podcast_script(subject)
        segments = self.parse_podcast_script(script)

        segment_files = []
        for index, segment in enumerate(segments):
            # Collect filenames generated for each segment
            segment_files.extend(list(self.synthesize_speech(segment['text'], segment['speaker'], index)))

        final_file = self.merge_audio(segment_files)
        return final_file






