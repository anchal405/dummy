from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from twilio.twiml.voice_response import VoiceResponse
from tts import text_to_speech
from transcriber import transcribe_audio_from_url  # ✅ Add this
import os

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/twilio/webhook")
async def call_handler(request: Request):
    print("📞 Incoming call webhook triggered.")

    # Dynamic text for TTS
    message = "Namaste! Aapne call kiya. Yeh FastAPI aur Azure ka TTS demo hai."

    # Generate audio
    text_to_speech(message)

    # Prepare TwiML to play generated audio
    response = VoiceResponse()
    response.play("https://0569-2405-201-6807-88d6-148c-b2ea-1136-9a1.ngrok-free.app/static/output_audio.wav")

    return Response(content=str(response), media_type="application/xml")


@app.post("/voice")
async def voice(request: Request):
    print("📞 /voice endpoint hit")
    twiml = """
    <Response>
        <Say voice="alice" language="en-IN">Please speak after the beep. Your voice will be recorded.</Say>
        <Record action="/recording" method="POST" maxLength="10" />
        <Say>I did not receive any input.</Say>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")


@app.post("/recording")
async def recording(request: Request):
    print("🎙️ /recording endpoint hit")
    form = await request.form()
    recording_url = form.get("RecordingUrl")

    if recording_url:
        transcription = transcribe_audio_from_url(recording_url)
        print("📝 Transcription:", transcription)

        response_twiml = f"""
        <Response>
            <Say voice="alice" language="en-IN">You said: {transcription}</Say>
        </Response>
        """
        return Response(content=response_twiml, media_type="application/xml")
    
    return Response(content="<Response><Say>Sorry, no recording received.</Say></Response>", media_type="application/xml")
