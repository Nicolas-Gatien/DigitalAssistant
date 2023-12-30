import speech_recognition
import pyttsx3

ENGINE = pyttsx3.init()

def listen():
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        return audio
def audio_to_text(audio):
    recognizer = speech_recognition.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        return text
    except:
        return ""

def speak(text):
    ENGINE.say(text)
    ENGINE.runAndWait()

while True:
    audio = listen()
    user_sentence = audio_to_text(audio)
    speak(user_sentence)
    print(user_sentence)