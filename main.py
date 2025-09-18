import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

if len(sys.argv) < 2:
    print("Usage: uv run main.py <prompt> [--verbose]")
    sys.exit(1)


def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Get file contents
    - Write contents to file
    - Run python files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    user_prompt = sys.argv[1]
    verbose_flag = None
    if len(sys.argv) > 2:
        verbose_flag = sys.argv[2]

    # get api
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # initialise client
    client = genai.Client(api_key=api_key)

    # add available functions
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # query and get response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    # # print response
    # print(f"Model response: {response.text}")

    # print function calls if they happened
    if response.function_calls:
        call_result = call_function(response.function_calls[0], verbose=True)
        if call_result is None:
            raise Exception("No result from function call")
        print(f"-> {call_result.parts[0].function_response.response}")

    if verbose_flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
