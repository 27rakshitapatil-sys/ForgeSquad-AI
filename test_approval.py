from langgraph.types import Command
from app.graph import graph
from google.genai.errors import ServerError

config = {"configurable": {"thread_id": "test-approval-1"}}

try:
    result = graph.invoke(
        {
            "goal": "Write a short paragraph about the benefits of cycling",
            "work": "",
            "next": "",
            "steps": 0,
            "background": "",
        },
        config,
    )

    while "__interrupt__" in result:
        info = result["__interrupt__"][0].value

        print("\n===== APPROVAL NEEDED =====")
        print(info["question"])
        print(info["work"])

        answer = "approve"
        print(f"\nAutomatically responding: {answer}")

        result = graph.invoke(
            Command(resume=answer),
            config,
        )

    print("\n===== APPROVAL TEST PASSED =====")
    print("\n===== FINAL WORK =====")
    print(result["work"])

except ServerError as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        print("\n===== APPROVAL TEST SKIPPED =====")
        print("Gemini API is temporarily unavailable (503).")
    else:
        raise