import subprocess
import os
import pyttsx3


def input_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Interpreting....")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
        except Exception as e:
            say("I did not get that. Can you say it again?")
            return "none"
        return query


def say(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def open_app(query):

    apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "command prompt": "start cmd",
        "powershell": "start powershell",
        "google chrome": "start chrome",
        "firefox": "start firefox",
        "microsoft edge": "start msedge",
        "spotify": "start spotify",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "pycharm": r'C:\Program Files\JetBrains\PyCharm Community Edition 2024.1\bin\pycharm64.exe',
        "intellij idea": r'C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.1\bin\idea64.exe',

    }

    for key in apps:
        if key in query.lower():
            say(f"Opening {key}...")
            command = apps[key]
            try:
                if "start" in command or command.endswith(".exe"):
                    subprocess.Popen(command, shell=True)
                else:
                    subprocess.Popen(["cmd", "/c", "start", command], shell=True)
            except Exception as e:
                say(f"Sorry, I couldn't open {key}. Error: {str(e)}")
            return

    say("Sorry, I don't recognize this application.")


