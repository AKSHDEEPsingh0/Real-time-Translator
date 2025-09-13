Real-time Voice Translator
This is a web-based, real-time voice translator built with Python and the Streamlit framework. It allows users to speak into their microphone and have their words instantly translated and spoken aloud in a different language.

The application is powered by a combination of powerful Python libraries for speech recognition, translation, and text-to-speech conversion.

Features
Voice-to-Voice Translation: Speak in one language and hear the translation spoken back in another.

Text-to-Text Translation: A separate section allows for direct text input and translation.

Multilingual Support: Supports a wide range of languages, including English, Spanish, French, German, Japanese, Hindi, Mandarin, Tamil, Telugu, Marathi, Bengali, and Arabic.

User-Friendly Interface: A simple and intuitive web interface for a seamless user experience.

Setup and Installation
To run this application locally, you need to have Python installed. It is highly recommended to use a virtual environment to manage dependencies.

Clone the repository:

git clone [https://github.com/AKSHDEEPsingh0/Real-time-Translator.git](https://github.com/AKSHDEEPsingh0/Real-time-Translator.git)
cd Real-time-Translator

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate

Install the required libraries:
The project uses a few key libraries that are listed in requirements.txt.

pip install -r requirements.txt

Install system-level dependencies for PyAudio:
On Ubuntu/Debian-based systems, you need to install a few system packages for the voice recognition to work correctly.

sudo apt-get update
sudo apt-get install build-essential libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0

How to Run the App
Once all dependencies are installed, you can launch the Streamlit application from your terminal:

streamlit run app.py

This will start a local web server and open a new browser tab with the translator app.

Libraries Used
Streamlit: For creating the web application interface.

SpeechRecognition: For converting spoken words into text.

Deep-Translator: For translating text from one language to another.

gTTS (Google Text-to-Speech): For converting the translated text back into spoken audio.

PyAudio: A low-level library for accessing the microphone.
