# transcriber.py
import azure.cognitiveservices.speech as speechsdk
import requests
import os

SPEECH_KEY = "8UL6S50wem1J5l8ORaEfRIeHv23gbfxpczy4iNoMg98dFtpfDxCGJQQJ99BFACGhslBXJ3w3AAAYACOGUUQ4"
SERVICE_REGION = "centralindia"  # Update as per your Azure region

# For local files
def transcribe_audio(file_path, language="en-IN"):
    print("🎙️ Starting transcription with Azure...")

    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
        speech_config.speech_recognition_language = language

        audio_config = speechsdk.audio.AudioConfig(filename=file_path)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = recognizer.recognize_once()

        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(f"✅ Transcription result: {result.text}")
            return result.text
        else:
            print(f"⚠️ Azure failed: {result.reason}")
            return None

    except Exception as e:
        print(f"❌ Azure exception: {e}")
        return None

# For Twilio audio URLs
def transcribe_audio_from_url(url, language="en-IN"):
    print("🌐 Downloading audio from:", url)
    try:
        response = requests.get(url + ".wav")  # Twilio appends .wav
        temp_path = "temp.wav"

        with open(temp_path, "wb") as f:
            f.write(response.content)

        transcription = transcribe_audio(temp_path, language=language)

        os.remove(temp_path)
        return transcription

    except Exception as e:
        print(f"❌ Failed to download or transcribe: {e}")
        return "Error occurred during transcription."
