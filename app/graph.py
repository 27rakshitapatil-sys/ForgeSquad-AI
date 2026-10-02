from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt
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

reviewer = Agent(
    name="Reviewer",
    role="You are a strict editor. Check the writer's paragraph for errors and clarity, then output the improved final paragraph only.",
)


class State(TypedDict):
    goal: str
    work: str
    next: str
    steps: int
    background: str


def memory_node(state: State):
    """Load relevant results from previous runs."""
    related = find_related(state["goal"], limit=2)

    if not related:
        background = "No related previous runs found."
    else:
        parts = []

        for past_goal, result in related:
            parts.append(
                f"Previous goal:\n{past_goal}\n\n"
                f"Previous result:\n{result}"
            )

        background = "\n\n--- Previous Run ---\n".join(parts)

    print("\n[Memory] Loaded related previous runs.")

    return {"background": background}


def supervisor_node(state: State):
    prompt = (
        f"Goal: {state['goal']}\n\n"
        f"Work done so far:\n{state['work'] or 'Nothing yet.'}\n\n"
        f"Relevant background from previous runs:\n"
        f"{state['background'] or 'None.'}\n\n"
        "Available workers: Researcher, Writer, Reviewer\n"
        "Which worker should act next? "
        "If the goal is fully achieved, answer DONE. "
        "Reply with ONLY one word: Researcher, Writer, Reviewer, or DONE. "
        "The usual order is Researcher, then Writer, then Reviewer."
    )

    answer = ask(
        prompt,
        system="You are a supervisor managing a team."
    )

    choice = answer.strip().strip(".")

    print(f"\n[Supervisor] chose: {choice}")

    if choice not in ("Researcher", "Writer", "Reviewer"):
        choice = "DONE"

    return {
        "next": choice,
        "steps": state["steps"] + 1,
    }


def researcher_node(state: State):
    task = (
        f"Goal: {state['goal']}\n\n"
        f"Background from past runs:\n"
        f"{state['background'] or 'None'}\n\n"
        f"Work so far:\n"
        f"{state['work'] or 'Nothing yet.'}"
    )

    result = researcher.run(task)

    return {
        "work": state["work"] + f"\n--- Researcher ---\n{result}\n"
    }


def writer_node(state: State):
    task = (
        f"Goal: {state['goal']}\n\n"
        f"Relevant previous work:\n"
        f"{state['background'] or 'None'}\n\n"
        f"Work so far:\n"
        f"{state['work']}"
    )

    result = writer.run(task)

    return {
        "work": state["work"] + f"\n--- Writer ---\n{result}\n"
    }


def reviewer_node(state: State):
    task = (
        f"Goal: {state['goal']}\n\n"
        f"Work so far:\n"
        f"{state['work']}"
    )

    result = reviewer.run(task)

    return {
        "work": state["work"] + f"\n--- Reviewer ---\n{result}\n"
    }


def approval_node(state: State):
    decision = interrupt({
        "question": "Approve the Researcher's notes before writing?",
        "work": state["work"],
    })

    if decision == "approve":
        return {"next": "Writer"}

    return {"next": "DONE"}


def route(state: State):
    if state["steps"] >= 6:
        return END

    if state["next"] == "DONE":
        return END

    return state["next"]


builder = StateGraph(State)

builder.add_node("memory", memory_node)
builder.add_node("supervisor", supervisor_node)
builder.add_node("Researcher", researcher_node)
builder.add_node("approval", approval_node)
builder.add_node("Writer", writer_node)
builder.add_node("Reviewer", reviewer_node)

builder.add_edge(START, "memory")
builder.add_edge("memory", "supervisor")

builder.add_conditional_edges("supervisor", route)

builder.add_edge("Researcher", "approval")
builder.add_conditional_edges("approval", route)

builder.add_edge("Writer", "supervisor")
builder.add_edge("Reviewer", "supervisor")

graph = builder.compile(
    checkpointer=MemorySaver()
)