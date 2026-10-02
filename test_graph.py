from app.graph import graph

config = {
    "configurable": {
        "thread_id": "test-graph-1"
    }
}

result = graph.invoke(
    {
        "goal": "Write a short paragraph about the benefits of walking",
        "work": "",
        "next": "",
        "steps": 0,
        "background": "",
    },
    config,
)

print("\n===== FINAL WORK =====")
print(result["work"])