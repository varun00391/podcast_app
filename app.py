import streamlit as st
import os

# Import your PodCastGenerator from your utils.py or the appropriate module
from utils import PodCastGenerator

def main():
    st.title("Podcast Generator")
    st.write("Enter a topic for your podcast in the field below. The podcast will be generated using two simulated hosts and will be playable directly in this app.")

    # Center the input field using Streamlit’s layout options (centered Markdown container)
    topic = st.text_input("Podcast Topic", "")

    if st.button("Generate Podcast"):
        if not topic.strip():
            st.error("Please enter a valid podcast topic.")
        else:
            # Create an instance of the PodCastGenerator
            podcaster = PodCastGenerator()

            # Use a spinner to indicate that processing is happening
            with st.spinner("Generating your podcast. This may take a moment..."):
                final_output = podcaster.create_podcast(topic)
            
            st.success("Podcast generated successfully!")
            
            # Ensure the final file exists and then play it
            if os.path.exists(final_output):
                with open(final_output, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
            else:
                st.error("Failed to generate the podcast.")

if __name__ == "__main__":
    main()
