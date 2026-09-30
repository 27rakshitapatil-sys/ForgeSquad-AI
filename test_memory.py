from app.graph import graph
from app.memory import save_run, get_runs

goal = "Write a short paragraph about the benefits of reading"

result = graph.invoke({
    "goal": goal,
    "work": "",
    "next": "",
    "steps": 0,
})

save_run(goal, result["work"])
print("\nSaved this run to memory.db")

print("\n===== LAST SAVED RUNS =====")
for created_at, saved_goal, saved_result in get_runs():
    print(f"{created_at} | {saved_goal}")