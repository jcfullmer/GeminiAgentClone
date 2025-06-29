import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

my_functions = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
model_name = "gemini-2.0-flash-001"










def main():
    load_dotenv()

    #args = sys.argv[1:]
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]
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
    for _ in range(20):
        response = get_response(client, messages,)
        for candidate in response.candidates:
            messages.append(candidate.content)
        if response.function_calls:
            function_call_part = response.function_calls[0]
            function_call_result = call_function(function_call_part,"--verbose" in sys.argv)
            messages.append(function_call_result)
            if function_call_result.parts and hasattr(function_call_result.parts[0], "function_response") and hasattr(function_call_result.parts[0].function_response, "response"):
                if "--verbose" in sys.argv:
                    print(f"-> {function_call_result.parts[0].function_response.response['result']}")
            else:
                raise Exception("ERROR: Function could not process.")
        else:   
            print("Response:")
            print(response.text)
            break
        if "--verbose" in sys.argv:
            prompt_token_count = response.usage_metadata.prompt_token_count
            candidates_token_count = response.usage_metadata.candidates_token_count
            print(f'User prompt: {user_prompt}\nPrompt tokens: {prompt_token_count}\nResponse tokens: {candidates_token_count}')


def     get_response(client, messages):
    response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt),
    )
    return response

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    if function_call_part.name not in my_functions:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    function_name = my_functions[function_call_part.name]
    function_call_part.args["working_directory"] = "./calculator"
    function_result = function_name(**function_call_part.args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string of the file content up to 10,000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to file, relative to the working directory. If not provided or file not found, the function will return an error.",
            ),
        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the inputted python file, constrained to the working directory .",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will run, relative to the working directory. If not provided or file not found, the function will return an error.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file with a file path first then contents arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file that will run, relative to the working directory. If not provided or file not found, the function will return an error.",
            ),
                "content": types.Schema(
                type=types.Type.STRING,
                description="The content that will be written to the file.",
            ),        
        },
    ),
)





available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)




if __name__ == "__main__":
     main()

