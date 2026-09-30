from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver
from app.agent import Agent
from app.llm import ask
from app.memory import find_related

researcher = Agent(
    name="Researcher",
    role="You are a researcher. Give 4 short, factual bullet points about the topic in the goal.",
)

writer = Agent(
    name="Writer",
    role="You are a writer. Using the work so far, write one short, clear paragraph that achieves the goal.",
)


class State(TypedDict):
    goal: str
    work: str
    next: str
    steps: int
    background: str

def supervisor_node(state: State):
    prompt = (
        f"Goal: {state['goal']}\n\n"
        f"Work done so far:\n{state['work'] or 'Nothing yet.'}\n\n"
        "Available workers: Researcher, Writer\n"
        "Which worker should act next? "
        "If the goal is fully achieved, answer DONE. "
        "Reply with ONLY one word: Researcher, Writer, or DONE."
    )
    answer = ask(prompt, system="You are a supervisor managing a team.")
    choice = answer.strip().strip(".")
    print(f"\n[Supervisor] chose: {choice}")
    if choice not in ("Researcher", "Writer"):
        choice = "DONE"
    return {"next": choice, "steps": state["steps"] + 1}


def researcher_node(state: State):
    task = (
        f"Goal: {state['goal']}\n\n"
        f"Background from past runs:\n{state['background'] or 'None'}\n\n"
        f"Work so far:\n{state['work']}"
    )
    result = researcher.run(task)
    return {"work": state["work"] + f"\n--- Researcher ---\n{result}\n"}


def writer_node(state: State):
    task = f"Goal: {state['goal']}\n\nWork so far:\n{state['work']}"
    result = writer.run(task)
    return {"work": state["work"] + f"\n--- Writer ---\n{result}\n"}

def approval_node(state: State):
    decision = interrupt({
        "question": "Approve the Researcher's notes before writing?",
        "work": state["work"],
    })
    if decision == "approve":
        return {"next": "Writer"}
    return {"next": "DONE"}

def route(state: State):
    if state["steps"] >= 6:  # safety limit
        return END
    if state["next"] == "DONE":
        return END
    return state["next"]


builder = StateGraph(State)
builder.add_node("supervisor", supervisor_node)
builder.add_node("Researcher", researcher_node)
builder.add_node("approval", approval_node)
builder.add_node("Writer", writer_node)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route)
builder.add_edge("Researcher", "approval")
builder.add_conditional_edges("approval", route)
builder.add_edge("Writer", "supervisor")

graph = builder.compile(checkpointer=MemorySaver())