import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

if len(sys.argv) < 2:
    print("Usage: uv run main.py <prompt> [--verbose]")
    sys.exit(1)


def main():
    # get user prompt
    user_prompt = sys.argv[1]
    verbose_flag = None
    if len(sys.argv) > 2:
        verbose_flag = sys.argv[2]

    # get api
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    # initialise client
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # query and get response
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    # print response
    print(response.text)

    if verbose_flag == "--verbose":
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
