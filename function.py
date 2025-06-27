import datetime
import pyttsx3
import os
import subprocess
import shutil


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


def show_time():
    strfTime = datetime.datetime.now().strftime("%H:%M:%S")
    say("The current time is display on screen sir...")
    print("Current time:", strfTime)


def show_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    say("The current date is display on screen sir....")
    print("Current date:", current_date)


def convert_speech_to_filename(name):
    name = name.lower().replace(" dot ", ".").strip()
    while "  " in name:
        name = name.replace("  ", " ")
    return name


def find_and_open(name):
    search_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),
        os.path.expanduser("~/Videos"),
        os.path.expanduser("~/Music")
    ]

    name = convert_speech_to_filename(name)
    print(f"Searching for: {name}")

    for path in search_paths:
        print(f"Checking in: {path}")

        for root, dirs, files in os.walk(path):

            if name.lower() in [d.lower() for d in dirs]:
                folder_path = os.path.join(root, name)
                subprocess.run(["explorer", folder_path], shell=True)
                say(f"Opening {name} folder, sir...")
                return

            for file in files:
                if name.lower() == file.lower():
                    file_path = os.path.join(root, file)
                    print(f"File found: {file_path}")
                    os.startfile(file_path)
                    say(f"Opening your {name} file, sir...")
                    return

    say(f"Sorry, I can't find the desired {name}.")


def save_item(name, new_name):
    search_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
    ]

    for path in search_paths:
        for root, dirs, files in os.walk(path):
            if name in dirs:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                say(f"Saved folder {name} as {new_name}.")
                return

            if name in files:
                old_path = os.path.join(root, name)
                new_path = os.path.join(root, new_name)
                os.rename(old_path, new_path)
                say(f"Saved file {name} as {new_name}.")
                return

    say(f"Sorry, I could not find {name}.")


def delete_item(name):
    search_paths = [
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Downloads"),
    ]

    name = name.strip().lower().replace(" dot ", ".")

    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for d in dirs:
                if d.lower() == name:
                    folder_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(folder_path)
                        say(f"Deleted folder {name}.")
                        return
                    except PermissionError:
                        say(f"Permission denied: Unable to delete {name}.")
                        return

            for f in files:
                if f.lower() == name:
                    file_path = os.path.join(root, f)
                    try:
                        os.remove(file_path)
                        say(f"Deleted file {name}.")
                        return
                    except PermissionError:
                        say(f"Permission denied: Unable to delete {name}.")
                        return

    say(f"Sorry, I could not find {name}.")
