from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL = "gemini-3.1-flash-lite"

_client = genai.Client()


def ask(prompt: str, system: str = "", tools: list = None) -> str:
    """Send a prompt to the LLM and return the text reply.
    If tools are given, the LLM can call them automatically."""
    config = {}
    if system:
        config["system_instruction"] = system
    if tools:
        config["tools"] = tools
    response = _client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=config or None,
    )
    return response.text