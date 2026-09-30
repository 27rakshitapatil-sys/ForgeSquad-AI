from app.agent import Agent
from app.llm import ask


class Supervisor:
    def __init__(self, workers: dict):
        self.workers = workers  # {"Researcher": Agent, "Writer": Agent}

    def choose_worker(self, goal: str, work_so_far: str) -> str:
        """Ask the LLM which worker should go next, or DONE."""
        names = ", ".join(self.workers.keys())
        prompt = (
            f"Goal: {goal}\n\n"
            f"Work done so far:\n{work_so_far or 'Nothing yet.'}\n\n"
            f"Available workers: {names}\n"
            "Which worker should act next? "
            "If the goal is fully achieved, answer DONE. "
            "Reply with ONLY one word: a worker name or DONE."
        )
        answer = ask(prompt, system="You are a supervisor managing a team.")
        return answer.strip().strip(".")

    def run(self, goal: str, max_steps: int = 5) -> str:
        work_so_far = ""
        for step in range(max_steps):
            choice = self.choose_worker(goal, work_so_far)
            print(f"\n[Supervisor] step {step + 1}: chose {choice}")
            if choice not in self.workers:
                break
            task = f"Goal: {goal}\n\nWork so far:\n{work_so_far}"
            result = self.workers[choice].run(task)
            work_so_far += f"\n--- {choice} ---\n{result}\n"
        return work_so_far