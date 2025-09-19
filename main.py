import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function, available_functions
from prompt import system_prompt
from config import LOOP_NUM


def main():
    # read in arguments
    verbose = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    # load env variables and get api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # initialise client and user prompt
    client = genai.Client(api_key=api_key)
    user_prompt = " ".join(args)
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # query and get response
    loop_index = 0
    while loop_index < 7:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            for candidate in response.candidates:
                messages.append(candidate.content)

            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(
                    f"Response tokens: {response.usage_metadata.candidates_token_count}"
                )

            if response.function_calls:
                for function_call_part in response.function_calls:
                    function_call_result = call_function(
                        function_call_part, verbose=True
                    )
                    if (
                        not function_call_result.parts
                        or not function_call_result.parts[0].function_response
                    ):
                        raise Exception("No result from function call")
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )

                    messages.append(
                        types.Content(
                            role="user",
                            parts=[function_call_result.parts[0]],
                        )
                    )
                loop_index += 1
                continue

            if response.text:
                print(f"Final response: {response.text}")
                break

        except Exception as e:
            print(f"Error: {e}")

        loop_index += 1


if __name__ == "__main__":
    main()
