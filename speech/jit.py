import speech_recognition as sr

# Initialize the recognizer
recognizer = sr.Recognizer()

# Initialize the microphone as the audio source
microphone = sr.Microphone()

# Continuously listen for speech input
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    print("Listening...")

    # Continuously listen for speech input
    while True:
        try:
            audio = recognizer.listen(source)
            print("Processing...")

            # Recognize speech using Google Web Speech API
            text = recognizer.recognize_google(audio)
            print("Recognized text:", text)

        except sr.UnknownValueError:
            print("Speech could not be understood")

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

