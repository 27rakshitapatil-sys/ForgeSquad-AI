import time
from functools import wraps
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.engineering.software_agents import (
    project_manager,
    architect,
    developer,
    database_engineer,
    tester,
    debugger,
    code_reviewer,
)


# =========================================================
# SETTINGS
# =========================================================

# Pause after each agent so token usage spreads across the minute.
AGENT_PAUSE_SECONDS = 5


# =========================================================
# FORGESQUAD AI — ENGINEERING STATE
# =========================================================

class EngineeringState(TypedDict):
    requirement: str
    project_plan: str
    architecture: str
    implementation: str
    database_design: str
    test_report: str
    debugging_report: str
    review: str
    test_status: str
    debug_count: int


# =========================================================
# HELPERS
# =========================================================

def compact(text: str, limit: int = 3500) -> str:
    """Limit previous agent output sent to Gemini."""

    if not text:
        return ""

    text = str(text)

    if len(text) <= limit:
        return text

    return text[:limit] + "\n\n[Previous output truncated.]"


def paced(fn):
    """Sleep briefly after a node finishes to avoid quota spikes."""

    @wraps(fn)
    def wrapper(state):
        result = fn(state)
        time.sleep(AGENT_PAUSE_SECONDS)
        return result

    return wrapper


# =========================================================
# PROJECT MANAGER
# =========================================================

def project_manager_node(state: EngineeringState):
    print("\n[Project Manager] analyzing requirement...")

    result = project_manager.run(
        f"""
User requirement:

{state['requirement']}

Create a concise engineering plan.

Include:
- Required features
- Engineering tasks
- Dependencies
- Implementation order

Keep it concise.
"""
    )

    return {"project_plan": result}


# =========================================================
# ARCHITECT
# =========================================================

def architect_node(state: EngineeringState):
    print("\n[Architect] designing architecture...")

    result = architect.run(
        f"""
User requirement:

{state['requirement']}

Project Manager plan:

{compact(state['project_plan'], 3000)}

Design the software architecture.

Include:
- Technology choices
- Project structure
- Major modules
- Data flow
- Important design decisions

Keep it concise.
"""
    )

    return {"architecture": result}


# =========================================================
# DEVELOPER
# =========================================================

def developer_node(state: EngineeringState):
    print("\n[Developer] implementing project...")

    previous_debug = (
        compact(state["debugging_report"], 2500)
        if state["debugging_report"]
        else "None"
    )

    result = developer.run(
        f"""
User requirement:

{state['requirement']}

Project plan:

{compact(state['project_plan'], 2500)}

Architecture:

{compact(state['architecture'], 3000)}

Database design:

{compact(state['database_design'], 2000) or "Not designed yet."}

Previous debugging report:

{previous_debug}

Implement the required software.

IMPORTANT:
- Inspect relevant existing files first.
- Preserve existing functionality.
- Use the available file tools.
- If a debugging report exists, fix the identified problem.
- Write implementation files when appropriate.
- Do not make unrelated changes.

After implementation, briefly summarize what was changed.
"""
    )

    return {"implementation": result}


# =========================================================
# DATABASE ENGINEER
# =========================================================

def database_engineer_node(state: EngineeringState):
    print("\n[Database Engineer] designing database...")

    result = database_engineer.run(
        f"""
User requirement:

{state['requirement']}

Architecture:

{compact(state['architecture'], 2500)}

Developer implementation:

{compact(state['implementation'], 2000)}

Determine whether persistent database storage is required.

If not required, return exactly:

NO DATABASE REQUIRED

Otherwise include:
- Database choice
- Entities
- Fields
- Relationships
- Constraints
- Indexing considerations

Keep the response concise.
"""
    )

    return {"database_design": result}


# =========================================================
# TESTER
# =========================================================

def tester_node(state: EngineeringState):
    print("\n[Tester] testing implementation...")

    # The Tester reads the real files with its tools, so it only
    # needs a short summary, not the full upstream documents.
    result = tester.run(
        f"""
User requirement:

{state['requirement']}

Implementation summary:

{compact(state['implementation'], 1500)}

Database:

{compact(state['database_design'], 500) or "None"}

Previous debugging report:

{compact(state['debugging_report'], 1000) or "None"}

Test the CURRENT project implementation.

IMPORTANT:
- Inspect the actual project files.
- Run appropriate safe test/validation commands.
- Inspect the actual command output.
- Identify real failures only.
- Do not modify source code.
- Do not assume a failure without evidence.
- Also run the application entry point with sample arguments, including one error case such as division by zero.
- A passing unit test suite alone is not enough for STATUS: PASS.

At the VERY END write exactly one:

STATUS: PASS

or

STATUS: FAIL

Use FAIL only for a confirmed error,
failing test, broken functionality, or
significant unresolved problem.

Keep the report concise.
"""
    )

    upper_result = result.upper()

    if "STATUS: FAIL" in upper_result:
        test_status = "FAIL"
    elif "STATUS: PASS" in upper_result:
        test_status = "PASS"
    else:
        test_status = "FAIL"

    print(f"[Tester] status: {test_status}")

    return {
        "test_report": result,
        "test_status": test_status,
    }


# =========================================================
# DEBUGGER
# =========================================================

def debugger_node(state: EngineeringState):
    print("\n[Debugger] investigating failure...")

    result = debugger.run(
        f"""
User requirement:

{state['requirement']}

Testing report:

{compact(state['test_report'], 3000)}

Implementation summary:

{compact(state['implementation'], 1500)}

Investigate the confirmed testing failure.

IMPORTANT:
- Inspect the relevant source files.
- Run diagnostic/test commands.
- Examine actual error output.
- Identify the root cause.
- Do not modify source code.

Give the Developer a precise targeted fix.

Return:
1. Error
2. Root cause
3. Affected component
4. Evidence
5. Proposed fix
6. Verification steps

Keep the response concise.
"""
    )

    return {
        "debugging_report": result,
        "debug_count": state["debug_count"] + 1,
    }


# =========================================================
# CODE REVIEWER
# =========================================================

def code_reviewer_node(state: EngineeringState):
    print("\n[Code Reviewer] performing final review...")

    result = code_reviewer.run(
        f"""
User requirement:

{state['requirement']}

Project plan:

{compact(state['project_plan'], 1500)}

Architecture:

{compact(state['architecture'], 2000)}

Implementation:

{compact(state['implementation'], 2500)}

Database:

{compact(state['database_design'], 800) or "None"}

Testing report:

{compact(state['test_report'], 2000)}

Debugging report:

{compact(state['debugging_report'], 1500) or "None"}

Perform the final software engineering review.

Check:
- Requirement coverage
- Correctness
- Security
- Maintainability
- Potential regressions
- Unnecessary complexity

Keep the final review concise.
"""
    )

    return {"review": result}


# =========================================================
# ROUTERS
# =========================================================

def after_developer_router(state: EngineeringState):
    """Design the database only once, not on every debug loop."""

    if not state["database_design"]:
        return "database"

    return "test"


def test_router(state: EngineeringState):

    if state["test_status"] == "PASS":
        print("\n[System] Tests passed -> Code Reviewer")
        return "review"

    if state["debug_count"] >= 3:
        print("\n[System] Maximum debugging attempts reached.")
        print("[System] Sending project to Code Reviewer.")
        return "review"

    print("\n[System] Tests failed -> Debugger")
    return "debug"


# =========================================================
# BUILD LANGGRAPH
# =========================================================

builder = StateGraph(EngineeringState)

builder.add_node("Project Manager", paced(project_manager_node))
builder.add_node("Architect", paced(architect_node))
builder.add_node("Developer", paced(developer_node))
builder.add_node("Database Engineer", paced(database_engineer_node))
builder.add_node("Tester", paced(tester_node))
builder.add_node("Debugger", paced(debugger_node))
builder.add_node("Code Reviewer", paced(code_reviewer_node))


# =========================================================
# FLOW
# =========================================================

builder.add_edge(START, "Project Manager")
builder.add_edge("Project Manager", "Architect")
builder.add_edge("Architect", "Developer")

# Developer -> Database Engineer (first pass only) or straight to Tester
builder.add_conditional_edges(
    "Developer",
    after_developer_router,
    {
        "database": "Database Engineer",
        "test": "Tester",
    },
)

builder.add_edge("Database Engineer", "Tester")

# Tester -> Debugger / Code Reviewer
builder.add_conditional_edges(
    "Tester",
    test_router,
    {
        "debug": "Debugger",
        "review": "Code Reviewer",
    },
)

builder.add_edge("Debugger", "Developer")
builder.add_edge("Code Reviewer", END)


# =========================================================
# COMPILE
# =========================================================

engineering_graph = builder.compile()