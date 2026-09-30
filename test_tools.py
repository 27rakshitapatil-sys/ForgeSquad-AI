from app.agent import Agent
from app.tools import calculator, get_time

math_agent = Agent(
    name="MathAgent",
    role="You are a helpful assistant. Use your tools whenever you need to calculate or check the time.",
    tools=[calculator, get_time],
)

answer = math_agent.run("What is 1234 * 5678, and what is the current time?")
print("\nANSWER:\n" + answer)