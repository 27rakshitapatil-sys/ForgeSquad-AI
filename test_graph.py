from app.graph import graph

result = graph.invoke({
    "goal": "Write a short paragraph about the benefits of walking",
    "work": "",
    "next": "",
    "steps": 0,
})

print("\n===== FINAL WORK =====")
print(result["work"])