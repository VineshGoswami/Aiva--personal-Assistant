import pywhatkit
import pyttsx3
import speech_recognition as sr


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
            return query.lower().strip()
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand what you said.")
            return "none"
        except sr.RequestError:
            say("Sorry, I'm having trouble with the speech service. Please try again later.")
            return "none"
        except Exception as e:
            say(f"An error occurred: {e}")
            return "none"


def say(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def open_youtube(query):
    query = query.lower().strip()

    if query in ["play video", "play a video"]:
        say("Please specify a video name.")
        video_query = input_command()
        if video_query == "none":
            return
        query = video_query

    video_name = query.replace("play", "").replace("this", "").replace("video", "").strip()

    if video_name:
        try:
            say(f"Playing {video_name} on YouTube...")
            pywhatkit.playonyt(video_name)
        except Exception as e:
            say(f"An error occurred while trying to play the video: {e}")
    else:
        say("Sorry, I couldn't recognize the video name.")


