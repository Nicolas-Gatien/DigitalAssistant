import speech_recognition

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


while True:
    audio = listen()
    user_sentence = audio_to_text(audio)
    print(user_sentence)