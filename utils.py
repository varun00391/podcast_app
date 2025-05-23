from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from prompt import SYSTEM_PROMPT
import re, os

from dotenv import load_dotenv

from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment


# load_dotenv()


# class PodCastGenerator():
#     def __init__(self,lang_code = 'a'):
    
#         """Initialize the Kokoro TTS pipeline and speaker voices."""
#         self.pipeline = KPipeline(lang_code=lang_code)
#         self.speaker_voices = {
#             "JANE": "af_bella",  # Example female voice
#             "MIKE": "am_adam"    # Example male voice
#         }

#     def generate_podcast_script(self,subject: str) -> str:
#         """Ask the LLM for a script of a podcast given by two hosts."""
#         messages = [
#             SystemMessage(content=SYSTEM_PROMPT),
#             HumanMessage(content=f"Here is the topic: {subject[:100]}")
#         ]

#         llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0.7,max_tokens=4000)

#         try:
#             response = llm.invoke(messages)
#         except Exception as e:
#             response = f"An error occurred: {e}"
#         return response.content

#     def parse_podcast_script(self,script: str):
#         """
#         Parse the podcast script to extract dialogue segments based on speaker labels.
        
#         Expects each line to begin with a speaker label like:
#         [JANE] Text...
#         [MIKE] Text...
        
#         Args:
#             script (str): The full podcast script.
            
#         Returns:
#             list of dict: Each dictionary contains 'speaker' and 'text' keys.
#         """
#         pattern = r'\[([A-Z]+)\]\s*(.*)'  # Correct regex pattern in one line
#         segments = []
#         for line in script.splitlines():
#             match = re.match(pattern, line)
#             if match:
#                 speaker = match.group(1)
#                 text = match.group(2).strip()
#                 segments.append({'speaker': speaker, 'text': text})
#         return segments

#     def synthesize_speech(self, text: str, speaker: str, index: int):
#         """Generate speech using Kokoro for each podcast segment and yield file names."""
#         voice = self.speaker_voices.get(speaker, "af_bella")  # Default fallback voice
#         generator = self.pipeline(text, voice=voice, speed=1, split_pattern=r'\n+')

#         for _, _, audio in generator:
#             filename = f"{index}_{speaker}.wav"
#             sf.write(filename, audio, 24000)
#             yield filename


#     def merge_audio(self,segment_files):
#         """Merge individual speech segments into a full podcast and clean up temporary files."""
#         podcast = AudioSegment.empty()
        
#         for file in segment_files:
#             segment = AudioSegment.from_file(file)
#             podcast += segment + AudioSegment.silent(duration=300)  # Add pauses for realism
        
#         final_output = "final_podcast.mp3"
#         podcast.export(final_output, format="mp3")
        
#         # Ensure final podcast exists before deleting temporary files
#         if os.path.exists(final_output):
#             for file in segment_files:
#                 os.remove(file)
        
#         return final_output
    
#     def create_podcast(self, subject: str):
#         """Full pipeline from script generation to final podcast output."""
#         script = self.generate_podcast_script(subject)
#         segments = self.parse_podcast_script(script)

#         segment_files = []
#         for index, segment in enumerate(segments):
#             # Collect filenames generated for each segment
#             segment_files.extend(list(self.synthesize_speech(segment['text'], segment['speaker'], index)))

#         final_file = self.merge_audio(segment_files)
#         return final_file


load_dotenv()


class PodCastGenerator():
    def __init__(self,lang_code = 'a'):
    
        """Initialize the Kokoro TTS pipeline and speaker voices."""
        self.pipeline = KPipeline(lang_code=lang_code)
        self.speaker_voices = {
            "JANE": "af_bella",  # Example female voice
            "MIKE": "am_adam"    # Example male voice
        }

    def generate_podcast_script(self,input_text: str) -> str:
        """Ask the LLM for a script of a podcast given by two hosts."""
        prompt_content = ""
        # if len(input_text) <= 150 and '\n' not in input_text:
        #     prompt_content = f"Here is the topic for the podcast: {input_text}"
        # elif len(input_text) > 150:
        #     prompt_content = f"Here is the detailed content for podcast: {input_text}"
        # else:
        #     raise ValueError("Either a subject or detailed content must be provided.")
        
        if len(input_text.splitlines()) > 1 or len(input_text) > 150: # If it has multiple lines OR is long
            prompt_content = f"Here is the detailed content for podcast: {input_text}"
        elif len(input_text) > 0: # This means it's short and single-line
            prompt_content = f"Here is the topic for the podcast: {input_text}"
        else: # Catches empty string after all checks
            raise ValueError("Input text cannot be empty.")

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt_content)   ##f"Here is the topic: {subject[:100]}")
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
    
    def create_podcast(self, input_text: str):
        """Full pipeline from script generation to final podcast output."""
        script = self.generate_podcast_script(input_text)
        segments = self.parse_podcast_script(script)

        segment_files = []
        for index, segment in enumerate(segments):
            # Collect filenames generated for each segment
            segment_files.extend(list(self.synthesize_speech(segment['text'], segment['speaker'], index)))

        final_file = self.merge_audio(segment_files)
        return final_file


# --- How to Run and Check ---
if __name__ == "__main__":
    podcast_gen = PodCastGenerator()

    # # --- Test Case 1: Simple Topic ---
    # print("\nAttempting to create podcast from a simple topic...")
    topic = "The importance of daily exercise for mental health"
    # final_podcast_path_topic = podcast_gen.create_podcast(input_text=topic)

    # if final_podcast_path_topic:
    #     print(f"\nPodcast generated successfully for topic! Check: {final_podcast_path_topic}")
    # else:
    #     print("\nFailed to generate podcast for topic.")

    # print("\n" + "="*50 + "\n")

    # # --- Test Case 2: Detailed Content ---
    # print("Attempting to create podcast from detailed content...")
    # detailed_text = """
    # Recent studies have shown a strong correlation between regular physical activity and improved mental well-being.
    # Even moderate exercise, such as a 30-minute brisk walk most days of the week, can significantly reduce symptoms
    # of anxiety and depression. This is attributed to several factors: exercise releases endorphins, which have mood-boosting
    # effects; it reduces stress hormones like cortisol; it improves sleep quality; and it can provide a sense of accomplishment
    # and self-esteem. Furthermore, engaging in exercise, especially outdoors, can offer a valuable break from daily stressors
    # and provide an opportunity for social interaction if done with others. Integrating exercise into one's routine is a
    # powerful tool for maintaining mental health.
    # """
    # final_podcast_path_detailed = podcast_gen.create_podcast(input_text=detailed_text)

    # if final_podcast_path_detailed:
    #     print(f"\nPodcast generated successfully from detailed content! Check: {final_podcast_path_detailed}")
    # else:
    #     print("\nFailed to generate podcast from detailed content.")






