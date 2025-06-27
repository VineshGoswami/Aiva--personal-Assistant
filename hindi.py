import speech_recognition as sr
from gtts import gTTS
import os
from datetime import datetime
import time
import pyglet
import google.generativeai as genai

genai.configure(api_key="AIzaSyCJ3g6NZG7Q2NRZv_-4yGxG7oe9GgncUnM")


PREDEFINED_RESPONSES = {
    "कैसा हो": "मैं अच्छा हूँ, धन्यवाद!",
    "समय बताओ": f"अभी समय है {datetime.now().strftime('%H:%M')}।",
    "बंद करो": "अलविदा!",
    "तुम्हारा नाम क्या है": "मेरा नाम आईवा है।",
    "भारत के प्रधानमंत्री कौन हैं": "भारत के प्रधानमंत्री नरेंद्र मोदी हैं।",
}


def recognize_hindi():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("कृपया बोलें...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language="hi-IN")
        print(f"आपने कहा: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("मुझे आपकी आवाज़ समझ नहीं आई।")
        return None
    except sr.RequestError:
        print("Google API से जुड़ने में समस्या हो रही है।")
        return None


def get_gemini_response(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response,
                                                             'text') else "क्षमा करें, मैं उत्तर देने में असमर्थ हूँ।"
    except Exception as e:
        print("Gemini API Error:", e)
        return "क्षमा करें, मैं अभी उत्तर देने में असमर्थ हूँ।"


def process_command_hindi(command):
    # Check if command is in predefined responses
    response = PREDEFINED_RESPONSES.get(command)

    if response is None:
        # If not predefined, ask Gemini AI in Hindi
        prompt = f"यह सवाल हिंदी में समझाकर जवाब दो: {command}"
        response = get_gemini_response(prompt)

    speak_hindi(response)

    if command == "बंद करो":
        speak_hindi("अलविदा!")
        exit()


def speak_hindi(text):
    tts = gTTS(text=text, lang='hi')
    filename = "response.mp3"
    tts.save(filename)

    music = pyglet.media.load(filename, streaming=False)
    player = music.play()
    time.sleep(music.duration)
    player.delete()
    os.remove(filename)


def main():
    print("AIVA सक्रिय है... (अंग्रेज़ी और हिंदी दोनों में आदेश दें)")
    while True:
        command = recognize_hindi()
        if command:
            process_command_hindi(command)


if __name__ == "__main__":
    main()
