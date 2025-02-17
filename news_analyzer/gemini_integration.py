from google import genai
from dotenv import load_dotenv
from google.genai import types
import os

load_dotenv()  # Load environment variables from .env

def send_prompt_to_gemini(system_prompt, user_prompt):
    """
    Sends a combined prompt (system prompt and user prompt) to the Gemini model and returns the response text.
    """
    combined_prompt = f"{system_prompt}\n\n{user_prompt}"  # Combine prompts

    api_key = os.getenv("GOOGLE_API_KEY")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=combined_prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=1000,
            response_mime_type='application/json',
        ),
    )
    return response.text
