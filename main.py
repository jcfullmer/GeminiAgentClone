import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    load_dotenv()

    args = sys.argv[1:]
    
    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here"')
        print('Example: python main.py "How do I create a notable resume?"')
        sys.exit(1)
    
    user_prompt = " ".join(args)
    api_key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = get_response(client, messages,)
    print("Response:")
    print(response.text)
    if "--verbose" in sys.argv:
        prompt_token_count = response.usage_metadata.prompt_token_count
        candidates_token_count = response.usage_metadata.candidates_token_count
        print(f'User prompt: {user_prompt}\nPrompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}')



def get_response(client, messages):
    response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages
    )
    prompt_token_count = response.usage_metadata.prompt_token_count
    candidates_token_count = response.usage_metadata.candidates_token_count
    return response

if __name__ == "__main__":
     main()