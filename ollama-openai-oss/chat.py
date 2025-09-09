import requests
import json
import subprocess
import argparse

# --- Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "gpt-oss:20b"

# System prompt from the original shell script
SYSTEM_PROMPT = """You are a knowledgeable, efficient, and direct AI assistant. Your core mission is to provide accurate, helpful, and actionable responses that directly address the user's needs.

## Key Principles:
- **Accuracy First**: If you don't know something or are uncertain, clearly state "I don't know" or "I'm not certain about this" rather than guessing
- **Be Specific**: Provide concrete, detailed answers with examples when appropriate
- **Stay Focused**: Address the user's actual question without unnecessary tangents or over-explanation
- **Actionable Guidance**: When possible, offer practical next steps or implementation advice

## Response Guidelines:
- Use clear, well-structured formatting with headers, bullets, or numbered lists when it improves readability
- Provide context when needed, but keep explanations concise and relevant
- If a task is complex, break it down into logical steps
- Cite sources or acknowledge limitations when discussing factual claims

## Interaction Style:
- Be professional yet approachable
- Adapt your technical level to match the user's apparent expertise
- Ask clarifying questions if the request is ambiguous
- Offer alternative approaches when relevant

Your goal is to be genuinely helpful while maintaining reliability and trustworthiness in every interaction."""


def render_output(text, use_glow=True):
    """
    Renders the given text using the 'glow' command-line tool if enabled.
    Falls back to a standard print if rendering is disabled or if glow fails.

    Args:
        text (str): The markdown-formatted text to render.
        use_glow (bool): Flag to determine whether to use glow for rendering.
    """
    if use_glow:
        try:
            print("\nAssistant:")
            # We let glow write directly to the terminal by removing `capture_output=True`.
            # This allows it to detect the interactive terminal and use colors.
            subprocess.run(
                ["glow", "-"],
                input=text,
                text=True,
                check=True,
            )
            # Add a newline for spacing after the glow output
            print()
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            # This is a fallback in case glow isn't found or returns an error
            print(f"Warning: 'glow' command failed ({e}). Falling back to raw text.")
            print(f"{text}\n")
    else:
        # If the --raw flag was used, just print the text as is.
        print(f"\nAssistant: {text}\n")


def run_chat_session(use_glow=True):
    """
    Initializes and runs a REPL chat session with the specified Ollama model.

    Args:
        use_glow (bool): Controls whether to render markdown output with glow.
    """
    chat_history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    print(f"✅ Starting chat session with '{MODEL_NAME}'.")
    print("   Type 'exit' or 'quit' to end the conversation.")
    print("-" * 60)

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!")
                break

            if not user_input.strip():
                continue

            chat_history.append({"role": "user", "content": user_input})

            payload = {
                "model": MODEL_NAME,
                "messages": chat_history,
                "stream": False,
                "options": {
                    "temperature": 0.0,
                    "repeat_penalty": 1.15,
                    "frequency_penalty": 0.2,
                    "presence_penalty": 0.1,
                    "stop": ["<|eot_id|>", "<|end_header_id|>", "\n\n\n"]
                }
            }

            response = requests.post(OLLAMA_ENDPOINT, json=payload)
            response.raise_for_status()

            response_data = response.json()
            assistant_message = response_data['choices'][0]['message']
            assistant_content = assistant_message['content'].strip()

            # The original print statement is now replaced with our render function.
            render_output(assistant_content, use_glow=use_glow)

            chat_history.append(assistant_message)

        except requests.exceptions.RequestException:
            print(f"\n❌ Error: Could not connect to the Ollama server at {OLLAMA_ENDPOINT}.")
            print("   Please ensure the Ollama container is running and accessible.")
            break
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break


if __name__ == "__main__":
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        description="A REPL chat client for Ollama with markdown rendering via glow."
    )
    # This flag, when present, will set 'render' to False.
    # By default, 'render' will be True, enabling glow.
    parser.add_argument(
        '--raw',
        dest='render',
        action='store_false',
        help="Disable markdown rendering and print raw model output."
    )
    args = parser.parse_args()

    # Start the chat session, passing in the value of the rendering flag.
    run_chat_session(use_glow=args.render)
