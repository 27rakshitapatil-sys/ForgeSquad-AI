from app.agent import Agent
from app.supervisor import Supervisor
from google.genai.errors import ServerError

researcher = Agent(
    name="Researcher",
    role="You are a researcher. Give 4 short, factual bullet points about the topic in the goal.",
)

writer = Agent(
    name="Writer",
    role="You are a writer. Using the work so far, write one short, clear paragraph that achieves the goal.",
)

team = Supervisor({"Researcher": researcher, "Writer": writer})

try:
    result = team.run("Write a short paragraph about the benefits of exercise")

    print("\n===== SUPERVISOR TEST PASSED =====")
    print("\n===== FINAL WORK =====")
    print(result)

except ServerError as e:
    if "503" in str(e) or "UNAVAILABLE" in str(e):
        print("\n===== SUPERVISOR TEST SKIPPED =====")
        print("Gemini API is temporarily unavailable (503).")
    else:
        raise