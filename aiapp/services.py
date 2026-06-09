from groq import Groq
from dotenv import load_dotenv
import os
import httpx

load_dotenv()


def ai_response(history):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
        timeout=httpx.Timeout(30.0, connect=10.0),
    )
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", messages=history
    )
    return response.choices[0].message.content
