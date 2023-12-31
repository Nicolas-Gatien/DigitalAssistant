import speech_recognition
import pyttsx3
import sys
import os
import importlib
import inspect
from assistant import Assistant
from skills.basic_skill import BasicSkill

ENGINE = pyttsx3.init()

def load_skills_from_folder():
    files_in_skills_directory = os.listdir("./skills")
    skill_files = []
    for file in files_in_skills_directory:
        if not file.endswith(".py"):
            continue
        forbidden_files = ["__init__.py", "basic_skill.py"]
        if file in forbidden_files:
            continue

        skill_files.append(file)

    skill_module_names = []
    for file in skill_files:
        skill_module_names.append(file[:-3])

    declared_skills = []
    for skill in skill_module_names:
        module = importlib.import_module('skills.' + skill)
        for name, member in inspect.getmembers(module):
            if not (inspect.isclass(member)):
                continue

            if not issubclass(member, BasicSkill):
                continue

            if member is BasicSkill:
                continue

            declared_skills.append(member())

    return declared_skills

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

declared_skills = load_skills_from_folder()
assistant = Assistant("config/api_keys.json", declared_skills)

while True:
    declared_skills = load_skills_from_folder()
    assistant.reload_skills(declared_skills)

    audio = listen()
    user_sentence = audio_to_text(audio)

    if user_sentence == "":
        continue

    print(f"Detected: {user_sentence}")

    prompt = user_sentence
    assistant_response = assistant.get_response(prompt)
    print(f"Responding: {assistant_response}")

    speak(assistant_response)