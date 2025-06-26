# tts.py
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv()

SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
SERVICE_REGION = os.getenv("AZURE_SERVICE_REGION")


def text_to_speech(text, filename="output_audio.wav"):
    print("🔁 Starting text-to-speech...")

    try:
        speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SERVICE_REGION)
        audio_config = speechsdk.audio.AudioOutputConfig(filename=filename)

        speech_config.speech_synthesis_voice_name = "hi-IN-SwaraNeural"

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        print("🔁 Sending request to Azure...")
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"[✔] Speech saved as {filename}")
        else:
            print(f"[✖] Error: {result.reason}")

    except Exception as e:
        print(f"[!!] Exception occurred: {e}")
if __name__ == "__main__":
    text_to_speech("Hello, this is a test using Azure TTS. Anchal ek chuutiya ladki h usko kuch nahi ata")
