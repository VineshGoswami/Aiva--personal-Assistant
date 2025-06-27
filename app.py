from flask import Flask, render_template, request, jsonify
import pyttsx3
import speech_recognition as sr
import os

app = Flask(__name__, template_folder="templates")  # Ensure Flask loads templates from the correct directory


def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def listen():
    """Capture voice input and return recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            return command
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "API unavailable"


def process_command(command):
    """Process the user command and execute actions."""
    response = "I did not understand that."

    if "hello" in command.lower():
        response = "Hello! How can I help you?"
    elif "open notepad" in command.lower():
        os.system("notepad.exe")
        response = "Opening Notepad."
    elif "play music" in command.lower():
        os.system("start wmplayer")
        response = "Playing music."

    speak(response)
    return response


@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")


@app.route("/send_text", methods=["POST"])
def send_text():
    """Handle text input from the user."""
    data = request.json
    user_input = data.get("text", "").strip()
    if user_input:
        response = process_command(user_input)
        return jsonify({"response": response})
    return jsonify({"response": "Invalid input."})


@app.route("/send_voice", methods=["POST"])
def send_voice():
    """Handle voice input from the user."""
    command = listen()
    if command:
        response = process_command(command)
        return jsonify({"command": command, "response": response})
    return jsonify({"command": "No input", "response": "Could not process voice input."})


if __name__ == "__main__":
    app.run(debug=True)
