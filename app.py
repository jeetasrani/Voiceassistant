import openai
import streamlit as st
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile

# Set up OpenAI API key
openai.api_key = 'YOUR_OPENAI_API_KEY'

# Streamlit app setup
st.title("Voice-based GPT Interface")
st.text("Speak into your microphone to interact with GPT")

# Speech recognition function
def recognize_speech_from_microphone():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
        try:
            st.write("Recognizing...")
            text = recognizer.recognize_google(audio)
            st.write(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            st.error("Could not request results; please check your internet connection.")
            return None

# GPT-3 interaction function
def get_gpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content'].strip()

# Main logic
if st.button("Speak and Get Response"):
    user_input = recognize_speech_from_microphone()
    if user_input:
        with st.spinner("Generating response..."):
            gpt_response = get_gpt_response(user_input)
            st.text_area("GPT Response", gpt_response)

            # Convert response to audio
            tts = gTTS(text=gpt_response, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
                tts.save(temp_audio.name)
                audio_path = temp_audio.name

            # Play audio
            st.audio(audio_path, format="audio/mp3")

            # Clean up temporary file
            os.remove(audio_path)
