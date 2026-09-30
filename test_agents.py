from app.agent import Agent

researcher = Agent(
    name="Researcher",
    role="You are a researcher. Give 4 short, factual bullet points about the topic you are given.",
)

writer = Agent(
    name="Writer",
    role="You are a writer. Turn the notes you are given into one short, clear paragraph.",
)

notes = researcher.run("Benefits of drinking water")
print("\nNOTES:\n" + notes)

summary = writer.run(notes)
print("\nSUMMARY:\n" + summary)