# this is for google gemini ai
from google import genai
import os
def google_ai(input):
    client=genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
    response=client.models.generate_content(
        model="gemini-2.0-flash",
        messages=[
            {"role": "system", "content": "you are a helpful assistant"},
            {"role": "user", "content": input},
        ]
    )
    return response.text