from app.llm import ask
from google.genai.errors import ServerError

try:
    result = ask("What is 2 + 2? Answer in one short sentence.")

    print("\n===== WRAPPER TEST PASSED =====")
    print(result)

except ServerError as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        print("\n===== WRAPPER TEST SKIPPED =====")
        print("Gemini API is temporarily unavailable (503).")
    else:
        raise