import sounddevice as sd
from scipy.io.wavfile import write
#this is for the local tests
# Settings
fs = 16000  # Sampling frequency = 16kHz (recommended for Azure)
seconds = 120  # Duration of the recording
filename = "output_audio.wav"

print("🎙️ Recording... Speak now!")
recording = sd.rec(int(seconds * fs), samplerate=fs, channels=1)
sd.wait()  # Wait until recording is finished
write(filename, fs, recording)  # Save as WAV file
print(f"✅ Recording saved to {filename}")
