import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
import argparse
from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function
import json


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    generate_content(client, messages, args)
    #print(available_functions)


def generate_content(client: OpenAI, messages: list, args) -> None:
    for _ in range(20):
        # call the model, handle responses, etc.
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
        )
        if not response.usage:
            raise RuntimeError("API response appears to be malformed")

        if args.verbose:
            print("User prompt:", messages[0])
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens)


        message = response.choices[0].message
        messages.append(message)

        if not message.tool_calls:
            print("Response:")
            print(message.content)
            return

        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            function_args = json.loads(tool_call.function.arguments or "{}")
            print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call,args.verbose)
            messages.append(result_message)
            if result_message["content"] == "":
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
    print("Reached Max iterations without exiting")
    sys.exit(1)
    

#def main():
#    print("Hello from buildanaiagent!")
    


if __name__ == "__main__":
    main()
