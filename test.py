# from kokoro import KPipeline
# import soundfile as sf

# # Initialize Kokoro TTS with the correct language code
# pipeline = KPipeline(lang_code="a")

# # Assign different voices for speakers
# speaker_voices = {
#     "JANE": "af_bella",  # Example female voice
#     "MIKE": "am_adam"   # Example male voice
# }

# def synthesize_speech(text: str, speaker: str, index: int):
#     """Generate speech using Kokoro for each podcast segment."""
#     voice = speaker_voices.get(speaker, "af_bella")  # Default fallback
#     generator = pipeline(text, voice=voice, speed=1, split_pattern=r'\n+')

#     for _, _, audio in generator:
#         sf.write(f"{index}_{speaker}.wav", audio, 24000)

# parsed_segments = [{'speaker': 'JANE', 'text': 'Hello and welcome to "Future Focus." I\'m your host, Jane. Today, we\'re exploring the impact of artificial intelligence on modern society. Joining me is Mike, an expert in AI and its applications. Mike, thanks for being here.'}, {'speaker': 'MIKE', 'text': "Thanks, Jane. It's great to be on the show."}, {'speaker': 'JANE', 'text': "So, let's dive right in. Artificial intelligence is transforming our world at an incredible pace. For those who might not be familiar, can you give us a quick overview of what AI is and how it's influencing our daily lives?"}, {'speaker': 'MIKE', 'text': 'Well, AI refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. From virtual assistants like Siri and Alexa to more complex systems used in healthcare and finance, AI is becoming increasingly integrated into our daily routines.'}, {'speaker': 'JANE', 'text': "That's a great point. I've noticed how often I use Siri to set reminders or get directions. But what about the more significant impacts, like on our workforce? There's been a lot of talk about job displacement due to automation. Can you speak to that?"}, {'speaker': 'MIKE', 'text': "Yes, definitely. Automation is a double-edged sword. On one hand, it can greatly increase efficiency and productivity. On the other hand, it does pose a risk to certain jobs, especially those that involve repetitive tasks. However, it's also creating new job opportunities in fields like AI development and maintenance."}, {'speaker': 'JANE', 'text': "That's a good point. I've heard about AI in healthcare being a game-changer. Can you share some examples of how AI is making a difference there?"}, {'speaker': 'MIKE', 'text': "Absolutely. AI is being used to analyze medical images, predict patient outcomes, and even help with drug discovery. It's the potential to significantly improve diagnosis accuracy and treatment effectiveness."}, {'speaker': 'JANE', 'text': "Wow, that's amazing. But with all this power comes great responsibility. What are some of the ethical considerations we need to be aware of with AI?"}, {'speaker': 'MIKE', 'text': "Ethical considerations are crucial. One of the main concerns is bias in AI decision-making. If the data used to train AI systems is biased, the AI's decisions can perpetuate those biases. Ensuring that AI systems are transparent and fair is a significant challenge we're facing."}, {'speaker': 'JANE', 'text': "That's really insightful. As we look to the future, what are some trends or developments you're excited about or concerned with?"}, {'speaker': 'MIKE', 'text': "I'm excited about the potential for AI to solve some of humanity's most pressing problems, like climate change and disease diagnosis. However, I'm also concerned about the need for robust regulations to ensure AI is used responsibly."}, {'speaker': 'JANE', 'text': "Well, Mike, it's been enlightening to get your perspective on AI. Before we go, can you summarize some of the key points we've discussed?"}, {'speaker': 'MIKE', 'text': "Sure. We've talked about the basics of AI, its impact on the workforce, its applications in healthcare, and the ethical considerations. AI is transforming our world in many ways, and it's crucial that we continue to have these conversations about how to harness its potential for good."}, {'speaker': 'JANE', 'text': 'Thanks, Mike, for shedding some light on this complex topic. And to our listeners, thank you for tuning in to this episode of "Future Focus." If you\'re interested in learning more about AI and its impacts, check out our resources page for some recommended reading and watching.'}]


# # Generate speech files for each speaker
# for idx, segment in enumerate(parsed_segments):
#     synthesize_speech(segment["text"], segment["speaker"], idx)

# from langchain_groq import ChatGroq
# from langchain.schema import SystemMessage, HumanMessage, AIMessage
# from prompt import SYSTEM_PROMPT
# import re

# from dotenv import load_dotenv

# load_dotenv()

# def generate_podcast(subject: str) -> str:
#     """Ask the LLM for a script of a podcast given by two hosts."""

#     messages = [
#     SystemMessage(content=SYSTEM_PROMPT),
#     HumanMessage(content=f"Here is the topic: {subject[:50]}")]

#      # Initialize the LLM (adjust the model parameters as needed).
#     llm = ChatGroq(model="meta-llama/llama-4-scout-17b-16e-instruct", temperature=0)

#     try:
#         response = llm.invoke(messages)
#     except Exception as e:
#         # Log or handle the error appropriately, perhaps falling back to a default message.
#         response = f"An error occurred: {e}"
#     return response.content

# def parse_podcast_script(script: str):
#     """
#     Parse the podcast script to extract dialogue segments based on speaker labels.
    
#     Expects each line to begin with a speaker label like:
#       [JANE] Text...
#       [MIKE] Text...
    
#     Args:
#         script (str): The full podcast script.
        
#     Returns:
#         list of dict: Each dictionary contains 'speaker' and 'text' keys.
#     """
#     pattern = r'\[([A-Z]+)\]\s*(.*)'  # Correct regex pattern in one line
#     segments = []
#     for line in script.splitlines():
#         match = re.match(pattern, line)
#         if match:
#             speaker = match.group(1)
#             text = match.group(2).strip()
#             segments.append({'speaker': speaker, 'text': text})
#     return segments

# if __name__ == "__main__":
#     # Example topic for generating a podcast script.
#     subject = "The impact of artificial intelligence on modern web development"
#     podcast_script = generate_podcast(subject)
    
#     print("Generated Podcast Script:")
#     print(podcast_script)

#     segments = parse_podcast_script(podcast_script)
#     print("Generated Parsed Segments")
#     print(segments)



import re
from kokoro import KPipeline
import soundfile as sf
from pydub import AudioSegment
from langchain.schema import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from prompt import SYSTEM_PROMPT
import re

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
    subject = "The impact of artificial intelligence on modern web development"
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
