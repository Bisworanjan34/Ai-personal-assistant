import os
from dotenv import load_dotenv
from groq import Groq
from google import genai

load_dotenv()


def gemini_test():
    # configure the gemini api key.
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    # generate a response.
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="What is the capital of France?",
    )
    print(response.text)


gemini_test()


def test_api():
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "you are work like a assistant"},
            {"role": "system", "content": "when start the first worldwar"},
        ],
    )
    print(response.choices[0].message.content)
