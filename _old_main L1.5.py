import os

from dotenv import load_dotenv
from openai import OpenAI
import argparse


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY environment variable not set")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    #prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to the LLM")
    args = parser.parse_args()
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[{"role": "user", "content": args.user_prompt}]
    )
    if response.usage == None:
        raise RuntimeError("Usage = None: (probably) failed API request")
    print("Prompt tokens: ", response.usage.prompt_tokens)
    print("Response tokens: ", response.usage.completion_tokens)
    print(response.choices[0].message.content)

#def main():
#    print("Hello from buildanaiagent!")
    


if __name__ == "__main__":
    main()
