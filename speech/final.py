import os
import pyaudio
import vosk
import json
import numpy as np
from scipy.signal import stft, istft
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont

# Define the Vosk model directory
MODEL_DIR = "C:/Users/HP/Downloads/vosk-model-small-en-us-0.15/vosk-model-small-en-us-0.15"

# Initialize the Vosk recognizer with the model
vosk_model = vosk.Model(MODEL_DIR)
recognizer = vosk.KaldiRecognizer(vosk_model, 16000)

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Define audio stream parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Start audio stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Create OLED display object
disp = Adafruit_SSD1306.SSD1306_128_64(rst=None)

# Initialize display
disp.begin()

# Clear display
disp.clear()
disp.display()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Initialize drawing object
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()

print("Listening...")

# Continuously listen, apply noise cancellation, and transcribe speech
while True:
    data = stream.read(CHUNK)
    if len(data) == 0:
        break
    
    # Convert raw bytes into 16-bit integer samples
    data_np = np.frombuffer(data, dtype=np.int16)
    
    # Apply noise cancellation (spectral subtraction)
    f, t, Zxx = stft(data_np, fs=RATE, nperseg=256)
    Zxx_denoised = Zxx - np.mean(Zxx, axis=1)[:, np.newaxis]
    _, data_denoised = istft(Zxx_denoised, fs=RATE)

    # Convert denoised data back to raw bytes
    data_denoised_bytes = data_denoised.astype(np.int16).tobytes()

    if recognizer.AcceptWaveform(data_denoised_bytes):
        result = json.loads(recognizer.Result())
        print("Transcription:", result["text"])
        
        # Clear previous text
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        
        # Display transcribed text on OLED
        draw.text((0, 0), "Transcription:", font=font, fill=255)
        draw.text((0, 16), result["text"], font=font, fill=255)
        disp.image(image)
        disp.display()

# Stop and close the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
