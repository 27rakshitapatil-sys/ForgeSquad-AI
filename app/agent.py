from app.llm import ask


class Agent:
    def __init__(self, name: str, role: str, tools: list = None):
        self.name = name
        self.role = role
        self.tools = tools or []

    def run(self, task: str) -> str:
        print(f"[{self.name}] working on: {task}")
        result = ask(task, system=self.role, tools=self.tools)
        print(f"[{self.name}] done")
        return result