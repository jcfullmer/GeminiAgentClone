import os
import sys
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)
prompt = sys.argv[1]

def get_response(*args):
    response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=args
    )
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    return f'{response.text}\nPrompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}'

print(get_response(prompt))