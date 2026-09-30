from langgraph.types import Command
from app.graph import graph

config = {"configurable": {"thread_id": "run-1"}}

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

# If the graph paused, ask the human
while "__interrupt__" in result:
    info = result["__interrupt__"][0].value
    print("\n===== APPROVAL NEEDED =====")
    print(info["question"])
    print(info["work"])
    answer = input("\nType 'approve' or 'reject': ").strip().lower()
    result = graph.invoke(Command(resume=answer), config)

print("\n===== FINAL WORK =====")
print(result["work"])