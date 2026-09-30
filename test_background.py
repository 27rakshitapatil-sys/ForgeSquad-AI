from app.graph import graph
from app.memory import find_related, save_run

goal = "Write a paragraph about the benefits of reading books"

# Look up related past runs and turn them into background text
matches = find_related(goal)
def clean(text):
    return text.replace("--- Researcher ---", "").replace("--- Writer ---", "").strip()

background = "\n\n".join(
    f"Past goal: {g}\nPast result: {clean(r)[:500]}" for g, r in matches
)
print(f"Using {len(matches)} past run(s) as background")

result = graph.invoke({
    "goal": goal,
    "work": "",
    "next": "",
    "steps": 0,
    "background": background,
})

save_run(goal, result["work"])
print("\n===== FINAL WORK =====")
print(result["work"])