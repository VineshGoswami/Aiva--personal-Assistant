import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import os
import threading
from main import authenticate_user, input_command, say, process_input, terminate

# Run the backend automatically in a separate thread
def start_backend():
    threading.Thread(target=authenticate_user, daemon=True).start()

# Function to speak text
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to listen for voice commands
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        status_label.config(text="Listening...")
        try:
            audio = recognizer.listen(source)
            command = recognizer.recognize_google(audio)
            status_label.config(text="Processing...")
            input_text.set(command)
            process_command(command)
        except sr.UnknownValueError:
            status_label.config(text="Could not understand audio")
        except sr.RequestError:
            status_label.config(text="API unavailable")

# Function to process commands
def process_command(command):
    response = process_input(command)
    output_text.insert(tk.END, f"You: {command}\n", "user")
    output_text.insert(tk.END, f"AIVA: {response}\n\n", "assistant")
    speak(response)

# Function to send text input as command
def send_command():
    user_input = entry.get()
    if user_input:
        output_text.insert(tk.END, f"You: {user_input}\n", "user")
        process_command(user_input)
        entry.delete(0, tk.END)
        output_text.yview(tk.END)

# Function to clear chat window
def clear_text():
    output_text.delete(1.0, tk.END)

# Function to exit application
def exit_app():
    terminate()
    root.destroy()

# Initialize GUI
root = tk.Tk()
root.title("AIVA - AI Assistant")
root.geometry("500x600")

input_text = tk.StringVar()
status_label = tk.Label(root, text="Starting backend...", font=("Arial", 12))
status_label.pack()

# Start backend on GUI launch
start_backend()
status_label.config(text="Ready")

# Chat Display Area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, state="normal", height=20, width=55)
output_text.tag_config("user", foreground="blue")
output_text.tag_config("assistant", foreground="green")
output_text.pack(padx=10, pady=10)

# Input Field and Send Button
entry = tk.Entry(root, width=40)
entry.pack(pady=5, side=tk.LEFT, padx=10)
send_button = tk.Button(root, text="Send", command=send_command)
send_button.pack(pady=5, side=tk.RIGHT, padx=10)

# Voice Input Button
btn_listen = tk.Button(root, text="🎤 Speak", command=listen, font=("Arial", 12))
btn_listen.pack(pady=5)

# Clear and Exit Buttons
btn_clear = tk.Button(root, text="Clear", command=clear_text, font=("Arial", 12))
btn_clear.pack(pady=5)

btn_exit = tk.Button(root, text="Exit", command=exit_app, font=("Arial", 12), fg="red")
btn_exit.pack(pady=5)

root.mainloop()