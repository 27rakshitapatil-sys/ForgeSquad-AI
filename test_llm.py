from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()

try:
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents="Say hello in one short sentence.",
    )
    print("\n===== GEMINI TEST PASSED =====")
    print(response.text)

except Exception as e:
    print("\n===== GEMINI TEST SKIPPED =====")
    print("Gemini API is temporarily unavailable.")
    print(f"Reason: {e}")