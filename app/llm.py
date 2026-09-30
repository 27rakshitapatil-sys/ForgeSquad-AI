import re
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError, ClientError

load_dotenv()

MODEL = "gemini-3.1-flash-lite"

# ---- Settings -------------------------------------------------------
MAX_RETRIES = 6            # attempts per request
BASE_DELAY = 2             # seconds, for 503 backoff
DEFAULT_429_WAIT = 60      # used when the server gives no retry delay
MAX_TOOL_ROUNDS = 8        # cap on automatic tool calls per request
# ---------------------------------------------------------------------

_client = genai.Client()


def _retry_delay_from_error(error_text: str) -> float:
    """Read 'Please retry in 52.69s' (or retryDelay '52s') from a 429."""
    match = re.search(r"retry in ([\d.]+)s", error_text, re.IGNORECASE)
    if not match:
        match = re.search(r"'retryDelay': '(\d+)s'", error_text)
    if match:
        return float(match.group(1)) + 2   # small safety margin
    return DEFAULT_429_WAIT


def ask(prompt: str, system: str = "", tools: list = None) -> str:
    """Send a prompt to the LLM and return the text reply.

    - 503 / UNAVAILABLE: exponential backoff.
    - 429 / RESOURCE_EXHAUSTED: waits the delay Google asks for.
    - Tool calling rounds are capped to limit hidden token usage.
    """

    config_kwargs = {}

    if system:
        config_kwargs["system_instruction"] = system

    if tools:
        config_kwargs["tools"] = tools
        config_kwargs["automatic_function_calling"] = (
            types.AutomaticFunctionCallingConfig(
                maximum_remote_calls=MAX_TOOL_ROUNDS
            )
        )

    config = types.GenerateContentConfig(**config_kwargs) if config_kwargs else None

    for attempt in range(MAX_RETRIES):
        is_last = attempt == MAX_RETRIES - 1

        try:
            response = _client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=config,
            )
            return response.text or ""

        except ServerError as e:
            error_text = str(e)

            if ("503" in error_text or "UNAVAILABLE" in error_text) and not is_last:
                delay = BASE_DELAY * (2 ** attempt)
                print(f"\n[Gemini] Temporary server error. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue

            raise

        except ClientError as e:
            error_text = str(e)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
                # A daily quota will not clear by waiting a minute.
                if "PerDay" in error_text:
                    raise RuntimeError(
                        "Daily Gemini quota exhausted. Wait for reset, "
                        "enable billing, or switch model."
                    ) from e

                if not is_last:
                    delay = _retry_delay_from_error(error_text)
                    print(f"\n[Gemini] Rate limit reached. Waiting {delay:.0f} seconds...")
                    time.sleep(delay)
                    continue

            raise

    return ""