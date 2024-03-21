import speech_recognition as sr
import pyaudio
from vosk import Model, KaldiRecognizer

# Initialize the Vosk speech recognition model with the pre-trained model file
model = Model("C:/Users/HP/Downloads/vosk-model-small-en-us-0.15")

# Initialize the recognizer with the model
recognizer = KaldiRecognizer(model, 16000)

# Initialize the microphone as the audio source
microphone = sr.Microphone()

# Continuously capture audio from the microphone and perform real-time transcription
recognizer.SetWords(True)
print("Listening...")

# Adjust for ambient noise before starting to listen
recognizer.SetMaxAlternatives(10)
recognizer.SetWords(True)

# Open the microphone stream
with microphone as source:
    # Adjust for ambient noise
    recognizer.AdjustWaveform(source)

    # Continuously read audio data from the stream
    while True:
        # Read audio data from the stream
        audio_data = source.stream.read(1024)

        # Perform speech recognition on the audio data
        recognizer.AcceptWaveform(audio_data)

        # Get the recognized result
        result = recognizer.Result()

        # Print the recognized text
        print("Recognized text:", result)
