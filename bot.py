import google.generativeai as genai
import absl.logging
from api import api_key
import pyttsx3
import sys

absl.logging.set_verbosity(absl.logging.ERROR)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")


def generate_text(query):


    try:
        result = model.generate_content(query)
        return result.text
    except Exception as e:
        return f"I am sorry, sir. I couldn't process the request: {e}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        response = generate_text(user_query)
        print(response)
