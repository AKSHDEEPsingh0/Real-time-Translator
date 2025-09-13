import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io

# Define a dictionary of supported languages
LANGUAGES = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'japanese': 'ja',
    'hindi': 'hi',
    'mandarin': 'zh-CN',
    'tamil': 'ta',
    'telugu': 'te',
    'marathi': 'mr',
    'bengali': 'bn',
    'arabic': 'ar'
}

# --- Function to handle Text-to-Speech and Audio Playback ---
# We'll generate a WAV file in memory to avoid writing to disk
def speak_translated_text(text, lang_code):
    """Converts the translated text to speech and returns it as a bytes object."""
    if not text:
        return
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        # Use an in-memory file-like object to store the audio data
        audio_stream = io.BytesIO()
        tts.write_to_fp(audio_stream)
        audio_stream.seek(0)
        return audio_stream.read()
    except Exception as e:
        st.error(f"Text-to-Speech error: {e}")
        return None

# --- Main Streamlit Web App ---
st.set_page_config(page_title="Voice Translator", layout="centered")

# --- Custom CSS for a professional look ---
st.markdown(
    """
    <style>
    body {
        background: url("https://images.unsplash.com/photo-1543285198-edb738c64573?q=80&w=2942&auto=format&fit=crop");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }
    .st-emotion-cache-183-f-e8b2g9c{
      background: rgba(255, 255, 255, 0.7);
    }
    .st-emotion-cache-163t72c{
      background-color: transparent;
    }
    .main-title {
        text-align: center;
        color: #FFFFFF;
        text-shadow: 2px 2px 4px #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .welcome-message {
        text-align: center;
        color: #FFFFFF;
        font-size: 1.2em;
        text-shadow: 1px 1px 2px #000000;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin-bottom: 2em;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 class="main-title">Welcome to the Universal Voice Translator</h1>', unsafe_allow_html=True)
st.markdown('<p class="welcome-message">Speak, translate, and communicate with ease.</p>', unsafe_allow_html=True)

# --- Language Selection ---
col1, col2 = st.columns(2)

with col1:
    source_lang_name = st.selectbox(
        "Source Language",
        options=list(LANGUAGES.keys()),
        index=0
    )
    source_lang_code = LANGUAGES.get(source_lang_name)

with col2:
    target_lang_name = st.selectbox(
        "Target Language",
        options=list(LANGUAGES.keys()),
        index=1
    )
    target_lang_code = LANGUAGES.get(target_lang_name)

st.markdown("---")

# --- Translation Logic ---
if "listening" not in st.session_state:
    st.session_state.listening = False

def start_listening():
    st.session_state.listening = True

# Single button to start the process
st.button("Start Listening", on_click=start_listening)

status_placeholder = st.empty()
user_text_placeholder = st.empty()
translated_text_placeholder = st.empty()

if st.session_state.listening:
    if not source_lang_code or not target_lang_code:
        st.error("Please select both a source and a target language.")
        st.session_state.listening = False
    else:
        status_placeholder.info("Listening... Speak now!")
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 5 # Set the pause duration to 5 seconds
            try:
                # Listen continuously until a pause of 5 seconds is detected
                audio_data = r.listen(source, timeout=5, phrase_time_limit=60) # Increased listening time
                
                status_placeholder.text("Speech captured. Recognizing...")
                
                # Speech-to-Text
                spoken_text = r.recognize_google(audio_data, language=source_lang_code)
                user_text_placeholder.info(f"You said ({source_lang_name}): {spoken_text}")

                # Translation
                translated_text = GoogleTranslator(
                    source=source_lang_code, 
                    target=target_lang_code
                ).translate(spoken_text)
                translated_text_placeholder.success(f"Translation ({target_lang_name}): {translated_text}")

                # Text-to-Speech and Playback
                audio_bytes = speak_translated_text(translated_text, target_lang_code)
                if audio_bytes:
                    st.audio(audio_bytes, format='audio/mp3', start_time=0)
                    status_placeholder.text("Translation spoken aloud.")
                
            except sr.WaitTimeoutError:
                status_placeholder.warning("Can't hear you. Please try again.")
            except sr.UnknownValueError:
                status_placeholder.warning("Could not understand audio. Please try again.")
            except sr.RequestError as e:
                status_placeholder.error(f"Speech service error: {e}")
            except Exception as e:
                status_placeholder.error(f"An unexpected error occurred: {e}")
            finally:
                st.session_state.listening = False

# --- Text Translation Section ---
st.markdown("---")
st.header("Or, Translate by Typing")

text_input = st.text_area("Enter text to translate:", height=150)

if st.button("Translate Text"):
    if not text_input:
        st.error("Please enter some text to translate.")
    elif not target_lang_code:
        st.error("Please select a target language.")
    else:
        try:
            # Translation for typed text. Source language is 'auto' for automatic detection.
            translated_text_typed = GoogleTranslator(
                source='auto', 
                target=target_lang_code
            ).translate(text_input)

            # Display the result
            st.success(f"Translation ({target_lang_name}):")
            st.write(translated_text_typed)

            # Text-to-Speech for typed text
            audio_bytes_typed = speak_translated_text(translated_text_typed, target_lang_code)
            if audio_bytes_typed:
                st.audio(audio_bytes_typed, format='audio/mp3', start_time=0)

        except Exception as e:
            st.error(f"An error occurred during text translation: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #FFFFFF;'>Powered by Streamlit, SpeechRecognition, and Deep-Translator</p>", unsafe_allow_html=True)
