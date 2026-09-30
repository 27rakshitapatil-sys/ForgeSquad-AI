from app.memory import find_related

matches = find_related("Write a paragraph about the benefits of reading books")

print(f"Found {len(matches)} related past run(s)")
for past_goal, result in matches:
    print("\nPAST GOAL:", past_goal)
    print("PAST RESULT (first 150 chars):", result[:150])