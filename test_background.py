from app.graph import graph
from app.memory import find_related, save_run
from google.genai.errors import ServerError

goal = "Write a paragraph about the benefits of reading books"

matches = find_related(goal)

def clean(text):
    return text.replace("--- Researcher ---", "").replace("--- Writer ---", "").strip()

background = "\n\n".join(
    f"Past goal: {g}\nPast result: {clean(r)[:500]}" for g, r in matches
)

print(f"Using {len(matches)} past run(s) as background")

config = {
    "configurable": {
        "thread_id": "test-background-1"
    }
}

try:
    result = graph.invoke(
        {
            "goal": goal,
            "work": "",
            "next": "",
            "steps": 0,
            "background": background,
        },
        config,
    )

    save_run(goal, result["work"])

    print("\n===== BACKGROUND TEST PASSED =====")
    print("\n===== FINAL WORK =====")
    print(result["work"])

except ServerError as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        print("\n===== BACKGROUND TEST SKIPPED =====")
        print("Gemini API is temporarily unavailable (503).")
    else:
        raise