import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import io
import pytesseract
from PIL import Image

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
def speak_translated_text(text, lang_code):
    """Converts the translated text to speech and returns it as a bytes object."""
    if not text:
        return None
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
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
    .chat-container {
        height: 400px;
        overflow-y: auto;
        padding: 10px;
        border: 1px solid #ccc;
        border-radius: 10px;
        background-color: rgba(255, 255, 255, 0.8);
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

# Conversation Mode
st.header("Conversation Mode")

# --- Initialize chat history and audio ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None

# --- Display chat messages from history on app rerun ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Display audio if available
if st.session_state.audio_bytes:
    st.audio(st.session_state.audio_bytes, format='audio/mp3', start_time=0)
    st.session_state.audio_bytes = None # Clear after playback

# --- Voice and Text Input ---
status_placeholder = st.empty()

if st.button("Start Real-time Translation"):
    if not source_lang_code or not target_lang_code:
        st.error("Please select both a source and a target language.")
    else:
        status_placeholder.info("Listening... Speak now!")
        
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            r.pause_threshold = 5 # Changed to 5 seconds
            
            try:
                audio_data = r.listen(source, timeout=5) #Removed phrase_time_limit
                
                status_placeholder.text("Speech captured. Recognizing...")
                
                spoken_text = r.recognize_google(audio_data, language=source_lang_code)
                
                # --- Add user message to chat history ---
                st.session_state.messages.append({"role": "user", "content": spoken_text})
                
                # --- Display user message in chat message container ---
                with st.chat_message("user"):
                    st.markdown(spoken_text)
                
                # --- Get translated text ---
                translated_text = GoogleTranslator(
                    source=source_lang_code, 
                    target=target_lang_code
                ).translate(spoken_text)

                # --- Display assistant response in chat message container ---
                with st.chat_message("assistant"):
                    st.markdown(translated_text)
                
                # --- Add assistant response to chat history ---
                st.session_state.messages.append({"role": "assistant", "content": translated_text})

                # --- Text-to-Speech and Playback ---
                st.session_state.audio_bytes = speak_translated_text(translated_text, target_lang_code)
                st.rerun()

            except sr.WaitTimeoutError:
                status_placeholder.warning("Can't hear you. Please try again.")
            except sr.UnknownValueError:
                status_placeholder.warning("Could not understand audio. Please try again.")
            except sr.RequestError as e:
                status_placeholder.error(f"Speech service error: {e}")
            except Exception as e:
                status_placeholder.error(f"An unexpected error occurred: {e}")
            finally:
                pass

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
            # --- Add user message to chat history ---
            st.session_state.messages.append({"role": "user", "content": text_input})

            # --- Display user message in chat message container ---
            with st.chat_message("user"):
                st.markdown(text_input)

            # Translation for typed text. Source language is 'auto' for automatic detection.
            translated_text_typed = GoogleTranslator(
                source='auto', 
                target=target_lang_code
            ).translate(text_input)

            # --- Display assistant response in chat message container ---
            with st.chat_message("assistant"):
                st.markdown(translated_text_typed)

            # --- Add assistant response to chat history ---
            st.session_state.messages.append({"role": "assistant", "content": translated_text_typed})

            # Text-to-Speech for typed text
            st.session_state.audio_bytes = speak_translated_text(translated_text_typed, target_lang_code)
            st.rerun()

        except Exception as e:
            st.error(f"An error occurred during text translation: {e}")

# --- Image Translation Section ---
st.markdown("---")
st.header("Or, Translate from an Image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)
    st.write("")

    if st.button("Translate Image Text"):
        with st.spinner("Extracting text..."):
            try:
                extracted_text = pytesseract.image_to_string(image)
                if extracted_text:
                    # Add user's image text to chat history
                    st.session_state.messages.append({"role": "user", "content": f"Image Text: {extracted_text}"})

                    # Display extracted text in the chat
                    with st.chat_message("user"):
                        st.markdown(f"Image Text: {extracted_text}")

                    # Translate the extracted text
                    translated_text = GoogleTranslator(
                        source='auto',
                        target=target_lang_code
                    ).translate(extracted_text)

                    # Add assistant's translated text to chat history
                    st.session_state.messages.append({"role": "assistant", "content": translated_text})

                    # Display translated text in the chat
                    with st.chat_message("assistant"):
                        st.markdown(translated_text)

                    # Text-to-Speech
                    st.session_state.audio_bytes = speak_translated_text(translated_text, target_lang_code)
                    st.rerun()

                else:
                    st.warning("No text could be extracted from the image. Please try another image.")

            except Exception as e:
                st.error(f"An error occurred during image translation: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #FFFFFF;'>Powered by Streamlit, SpeechRecognition, and Deep-Translator</p>", unsafe_allow_html=True)
