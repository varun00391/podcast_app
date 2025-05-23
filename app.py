# import streamlit as st
# import os

# # Import your PodCastGenerator from your utils.py or the appropriate module
# from utils import PodCastGenerator

# def main():
#     st.title("Podcast Generator")
#     st.write("Enter a topic for your podcast in the field below. The podcast will be generated using two simulated hosts and will be playable directly in this app.")

#     # Center the input field using Streamlit’s layout options (centered Markdown container)
#     topic = st.text_input("Podcast Topic", "")

#     if st.button("Generate Podcast"):
#         if not topic.strip():
#             st.error("Please enter a valid podcast topic.")
#         else:
#             # Create an instance of the PodCastGenerator
#             podcaster = PodCastGenerator()

#             # Use a spinner to indicate that processing is happening
#             with st.spinner("Generating your podcast. This may take a moment..."):
#                 final_output = podcaster.create_podcast(topic)
            
#             st.success("Podcast generated successfully!")
            
#             # Ensure the final file exists and then play it
#             if os.path.exists(final_output):
#                 with open(final_output, "rb") as audio_file:
#                     audio_bytes = audio_file.read()
#                 st.audio(audio_bytes, format="audio/mp3")
#             else:
#                 st.error("Failed to generate the podcast.")

# if __name__ == "__main__":
#     main()


# import streamlit as st
# import os

# # Import your PodCastGenerator from your utils.py or the appropriate module
# # Make sure your PodCastGenerator is in a file named 'utils.py'
# # and contains the latest create_podcast method definition
# from utils import PodCastGenerator

# def main():
#     st.set_page_config(layout="wide") # Use wide layout for better column display
#     st.title("Podcast Generator")
#     st.write("Choose to generate a podcast from either a simple topic or detailed content.")

#     # Create two columns
#     col1, col2 = st.columns([1, 2]) # col1 will be 1/3 width, col2 will be 2/3 width

#     input_type = None
#     user_input = ""

#     with col1:
#         st.header("Generate by Topic")
#         st.write("Enter a simple topic for your podcast.")
#         topic_input = st.text_input("Podcast Topic", key="topic_input")

#         if st.button("Generate Podcast (Topic)", key="generate_topic_btn"):
#             if not topic_input.strip():
#                 st.error("Please enter a valid podcast topic.")
#             else:
#                 input_type = 'topic'
#                 user_input = topic_input

#     with col2:
#         st.header("Generate by Detailed Content")
#         st.write("Provide a detailed paragraph or story for your podcast script.")
#         detailed_content_input = st.text_area("Detailed Content", height=250, key="detailed_content_input")

#         if st.button("Generate Podcast (Detailed Content)", key="generate_detailed_btn"):
#             if not detailed_content_input.strip():
#                 st.error("Please enter valid detailed content.")
#             else:
#                 input_type = 'detailed_content'
#                 user_input = detailed_content_input

#     # Logic to generate podcast, triggered after a button is pressed
#     if input_type:
#         # Create an instance of the PodCastGenerator
#         podcaster = PodCastGenerator()

#         # Use a spinner to indicate that processing is happening
#         with st.spinner("Generating your podcast. This may take a moment..."):
#             final_output = None
#             try:
#                 if input_type == 'topic':
#                     final_output = podcaster.create_podcast(subject=user_input)
#                 elif input_type == 'detailed_content':
#                     final_output = podcaster.create_podcast(detailed_content=user_input)
#             except ValueError as e:
#                 st.error(f"Error: {e}")
#             except Exception as e:
#                 st.error(f"An unexpected error occurred: {e}")

#         if final_output and os.path.exists(final_output):
#             st.success("Podcast generated successfully!")

#             st.subheader("Listen to your podcast:")
#             with open(final_output, "rb") as audio_file:
#                 audio_bytes = audio_file.read()
#             st.audio(audio_bytes, format="audio/mp3")

#             # Optional: Add a download button
#             st.download_button(
#                 label="Download Podcast",
#                 data=open(final_output, "rb").read(),
#                 file_name="generated_podcast.mp3",
#                 mime="audio/mp3"
#             )

#         elif final_output is None: # This would be the case if an error occurred in podcast_gen.create_podcast
#              # Error message already displayed by try-except block
#              pass
#         else:
#             st.error("Failed to generate the podcast. Please check the console for more details.")


# if __name__ == "__main__":
#     main()


################################# new version #######################
# import streamlit as st
# import os

# # Import your PodCastGenerator from your utils.py or the appropriate module
# from utils import PodCastGenerator

# def main():
#     st.set_page_config(layout="wide") # Use wide layout for better column display
#     st.title("Podcast Generator")
#     st.write("Choose to generate a podcast from either a simple topic or detailed content.")

#     # Create two columns: one for inputs, one for output
#     col_inputs, col_output = st.columns([1, 2]) # col_inputs will be 1/3 width, col_output will be 2/3 width

#     # Initialize session state for input type and user input if not already set
#     # This helps retain the state across reruns, crucial for triggering generation after button clicks
#     if 'input_type' not in st.session_state:
#         st.session_state['input_type'] = None
#     if 'user_input' not in st.session_state:
#         st.session_state['user_input'] = ""
#     if 'generate_triggered' not in st.session_state:
#         st.session_state['generate_triggered'] = False


#     # --- Left Column: Inputs ---
#     with col_inputs:
#         st.header("Generate Podcast Script")

#         # Option 1: Topic Input
#         st.subheader("1. From a Simple Topic")
#         st.write("Enter a simple topic for your podcast.")
#         topic_input = st.text_input("Podcast Topic", key="topic_input")

#         # Button for Topic Generation
#         if st.button("Generate Podcast from Topic", key="generate_topic_btn"):
#             if not topic_input.strip():
#                 st.error("Please enter a valid podcast topic.")
#                 st.session_state['generate_triggered'] = False # Reset trigger if input is invalid
#             else:
#                 st.session_state['input_type'] = 'topic'
#                 st.session_state['user_input'] = topic_input
#                 st.session_state['generate_triggered'] = True # Set trigger to start generation

#         st.markdown("---") # Separator for visual clarity

#         # Option 2: Detailed Content Input
#         st.subheader("2. From Detailed Content")
#         st.write("Provide a detailed paragraph or story for your podcast script.")
#         detailed_content_input = st.text_area("Detailed Content", height=250, key="detailed_content_input")

#         # Button for Detailed Content Generation
#         if st.button("Generate Podcast from Detailed Content", key="generate_detailed_btn"):
#             if not detailed_content_input.strip():
#                 st.error("Please enter valid detailed content.")
#                 st.session_state['generate_triggered'] = False # Reset trigger if input is invalid
#             else:
#                 st.session_state['input_type'] = 'detailed_content'
#                 st.session_state['user_input'] = detailed_content_input
#                 st.session_state['generate_triggered'] = True # Set trigger to start generation

#     # --- Right Column: Output ---
#     with col_output:
#         st.header("Generated Podcast")

#         # Logic to generate podcast, triggered only if 'generate_triggered' is True
#         if st.session_state['generate_triggered']:
#             # Reset the trigger immediately so it doesn't re-run endlessly
#             st.session_state['generate_triggered'] = False

#             # Create an instance of the PodCastGenerator
#             podcaster = PodCastGenerator()

#             # Use a spinner to indicate that processing is happening
#             with st.spinner("Generating your podcast. This may take a moment..."):
#                 final_output = None
#                 try:
#                     if st.session_state['input_type'] == 'topic':
#                         final_output = podcaster.create_podcast(subject=st.session_state['user_input'])
#                     elif st.session_state['input_type'] == 'detailed_content':
#                         final_output = podcaster.create_podcast(detailed_content=st.session_state['user_input'])
#                 except ValueError as e:
#                     st.error(f"Error generating podcast: {e}")
#                 except Exception as e:
#                     st.error(f"An unexpected error occurred: {e}")

#             if final_output and os.path.exists(final_output):
#                 st.success("Podcast generated successfully!")

#                 st.subheader("Listen to your podcast:")
#                 with open(final_output, "rb") as audio_file:
#                     audio_bytes = audio_file.read()
#                 st.audio(audio_bytes, format="audio/mp3")

#                 # Optional: Add a download button
#                 st.download_button(
#                     label="Download Podcast",
#                     data=open(final_output, "rb").read(),
#                     file_name="generated_podcast.mp3",
#                     mime="audio/mp3"
#                 )
#             elif final_output is None:
#                 # Error message already displayed by try-except block
#                 pass
#             else:
#                 st.error("Failed to generate the podcast. Please check the console for more details.")
#         else:
#             st.info("Enter content on the left and click a 'Generate Podcast' button to start.")


# if __name__ == "__main__":
#     main()


#######################  ########################

import streamlit as st
import os
import io # Still useful if you decide to add download later, but not strictly needed for just playback

# Import your PodCastGenerator from your utils.py or the appropriate module
from utils import PodCastGenerator

def main():
    st.set_page_config(layout="wide") # Use wide layout for better column display
    st.title("Podcast Generator")
    st.write("Enter your podcast idea below. You can provide a simple topic or detailed content, and the app will generate a podcast script and audio for you.")

    # Create two columns: one for inputs, one for output
    col_inputs, col_output = st.columns([1, 2]) # col_inputs will be 1/3 width, col_output will be 2/3 width

    # Initialize session state for input content and trigger if not already set
    if 'user_input_content' not in st.session_state:
        st.session_state['user_input_content'] = ""
    if 'generate_triggered' not in st.session_state:
        st.session_state['generate_triggered'] = False
    # Store the path to the generated podcast to reuse for playback (no download needed now)
    if 'generated_podcast_path' not in st.session_state:
        st.session_state['generated_podcast_path'] = None

    # --- Left Column: Single Input Area ---
    with col_inputs:
        st.header("Your Podcast Idea")

        st.write("Type a **short topic** (e.g., 'The benefits of reading') or a **detailed paragraph/story** that you want your podcast to be about.")
        user_input_text = st.text_area(
            "Enter your topic or detailed content here:",
            value=st.session_state['user_input_content'],
            height=250,
            placeholder="e.g., 'The history of space exploration' or 'Recent advancements in AI are transforming industries globally. AI-powered tools are automating tasks, enhancing decision-making, and creating new opportunities across various sectors...' ",
            key="single_input_area"
        )

        # Update session state with current input
        st.session_state['user_input_content'] = user_input_text

        # Single Generate Podcast button
        if st.button("Generate Podcast", key="generate_podcast_btn"):
            if not st.session_state['user_input_content'].strip():
                st.error("Please enter some text to generate the podcast.")
                st.session_state['generate_triggered'] = False # Reset trigger if input is invalid
                st.session_state['generated_podcast_path'] = None # Clear previous output path
            else:
                st.session_state['generate_triggered'] = True # Set trigger to start generation
                st.session_state['generated_podcast_path'] = None # Clear previous output path when new generation starts

    # --- Right Column: Output ---
    with col_output:
        st.header("Generated Podcast")

        # Logic to generate podcast, triggered only if 'generate_triggered' is True
        if st.session_state['generate_triggered']:
            # Reset the trigger immediately so it doesn't re-run endlessly
            st.session_state['generate_triggered'] = False

            # Create an instance of the PodCastGenerator
            podcaster = PodCastGenerator()

            # Use a spinner to indicate that processing is happening
            with st.spinner("Generating your podcast. This may take a moment..."):
                final_output = None
                try:
                    # Pass the single user input text directly to create_podcast
                    final_output = podcaster.create_podcast(input_text=st.session_state['user_input_content'])
                except ValueError as e:
                    st.error(f"Error generating podcast: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")

            if final_output and os.path.exists(final_output):
                st.session_state['generated_podcast_path'] = final_output # Store the path
                st.success("Podcast generated successfully!")

                st.subheader("Listen to your podcast:")
                with open(final_output, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

                # --- DOWNLOAD BUTTON REMOVED HERE ---
            elif final_output is None:
                pass # Error message already displayed by try-except block
            else:
                st.error("Failed to generate the podcast. Please check the console for more details.")

        # Display info message only if no generation has happened or it failed
        # This condition now correctly includes checking if there's a podcast path to display
        if not st.session_state['generate_triggered'] and st.session_state['generated_podcast_path'] is None:
            st.info("Enter your topic or detailed content on the left, then click 'Generate Podcast'.")


if __name__ == "__main__":
    main()