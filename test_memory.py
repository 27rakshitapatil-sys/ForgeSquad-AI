from app.graph import graph
from app.memory import save_run, get_runs
from google.genai.errors import ServerError

goal = "Write a short paragraph about the benefits of reading"

config = {
    "configurable": {
        "thread_id": "test-memory-1"
    }
}

try:
    result = graph.invoke(
        {
            "goal": goal,
            "work": "",
            "next": "",
            "steps": 0,
            "background": "",
        },
        config,
    )

    save_run(goal, result["work"])

    print("\n===== MEMORY TEST PASSED =====")
    print("\nSaved this run to memory.db")

    print("\n===== LAST SAVED RUNS =====")
    for created_at, saved_goal, saved_result in get_runs():
        print(f"{created_at} | {saved_goal}")

except ServerError as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        print("\n===== MEMORY TEST SKIPPED =====")
        print("Gemini API is temporarily unavailable (503).")
    else:
        raise