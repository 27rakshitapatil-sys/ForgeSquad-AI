from pathlib import Path
from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.engineering.software_agents import SOFTWARE_ENGINEERING_SQUAD


# ============================================================
# PROJECT FILE COLLECTION SETTINGS
# ============================================================

MAX_PROJECT_FILE_CHARS = 20000

IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}

IGNORED_FILE_NAMES = {
    ".DS_Store",
}

IGNORED_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".db",
    ".sqlite",
    ".sqlite3",
}


# ============================================================
# ENGINEERING STATE
# ============================================================

class EngineeringState(TypedDict):
    requirement: str
    project_root: str

    project_plan: str
    architecture: str
    implementation: str
    database_design: str

    test_report: str
    debugging_report: str
    review: str

    test_status: str
    debug_count: int

    generated_files: dict[str, str]


# ============================================================
# PROJECT FILE COLLECTION
# ============================================================

def collect_generated_files(project_root: str) -> dict[str, str]:
    """
    Collect only the files generated inside the current
    engineering run's isolated project directory.
    """

    workspace_dir = Path.cwd().resolve() / "workspace"
    project_dir = (workspace_dir / project_root).resolve()

    if not project_dir.exists():
        print(
            f"[Code Reviewer] project directory not found: "
            f"{project_root}"
        )
        return {}

    if not project_dir.is_dir():
        print(
            f"[Code Reviewer] project path is not a directory: "
            f"{project_root}"
        )
        return {}

    generated_files = {}

    for path in project_dir.rglob("*"):

        if not path.is_file():
            continue

        # Ignore unwanted directories.
        if any(
            ignored in path.parts
            for ignored in IGNORED_DIRECTORIES
        ):
            continue

        if path.name in IGNORED_FILE_NAMES:
            continue

        if path.suffix.lower() in IGNORED_SUFFIXES:
            continue

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace",
            )
        except Exception:
            continue

        if len(content) > MAX_PROJECT_FILE_CHARS:
            omitted = len(content) - MAX_PROJECT_FILE_CHARS

            content = (
                content[:MAX_PROJECT_FILE_CHARS]
                + f"\n\n"
                f"[... file truncated, "
                f"{omitted} more characters ...]"
            )

        # Store paths relative to the generated project root.
        relative_path = path.relative_to(project_dir)

        generated_files[
            relative_path.as_posix()
        ] = content

    generated_files = dict(
        sorted(generated_files.items())
    )

    print(
        f"[Code Reviewer] captured "
        f"{len(generated_files)} project files "
        f"from {project_root}."
    )

    return generated_files


# ============================================================
# PROJECT MANAGER
# ============================================================

def project_manager_node(state: EngineeringState):

    requirement = state["requirement"]

    prompt = f"""
You are the Project Manager of an autonomous software
engineering squad.

User requirement:
{requirement}

Create a clear software development plan.

Include:

1. Understanding of the requirement
2. Main features
3. Functional requirements
4. Non-functional requirements
5. Development tasks
6. Testing requirements
7. Expected final deliverables

Do not write code.
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Project Manager"
    ].run(prompt)

    return {
        "project_plan": result
    }


# ============================================================
# ARCHITECT
# ============================================================

def architect_node(state: EngineeringState):

    requirement = state["requirement"]
    project_plan = state["project_plan"]
    project_root = state["project_root"]

    prompt = f"""
You are the Software Architect of an autonomous
software engineering squad.

User requirement:
{requirement}

Project Manager plan:
{project_plan}

The isolated project directory for THIS run is:

{project_root}

Design the architecture for the software.

Include:

1. Technology choices
2. Project structure
3. Main modules
4. Responsibilities of each module
5. Data flow
6. Testing structure
7. How the project will be executed

IMPORTANT:

All implementation files must eventually be created
inside:

{project_root}

Do not write code yet.
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Architect"
    ].run(prompt)

    return {
        "architecture": result
    }


# ============================================================
# DEVELOPER
# ============================================================

def developer_node(state: EngineeringState):

    requirement = state["requirement"]
    architecture = state["architecture"]
    project_plan = state["project_plan"]
    project_root = state["project_root"]

    prompt = f"""
You are the Developer of an autonomous software
engineering squad.

User requirement:
{requirement}

Project Manager plan:
{project_plan}

Architecture:
{architecture}

============================================================
CURRENT PROJECT ROOT
============================================================

{project_root}

============================================================

YOUR TASK
============================================================

Actually BUILD the software.

This is not a theoretical response.

You must create the actual project files using the
available write_project_file tool.

ALL files for this engineering run MUST be created
inside:

{project_root}

Do NOT create files outside this directory.

For example:

{project_root}/src/main.py
{project_root}/src/calculator.py
{project_root}/tests/test_calculator.py
{project_root}/README.md

Use write_project_file for every source code,
test, configuration, and documentation file that
the project needs.

Requirements:

1. Implement the requested functionality.
2. Create a clean project structure.
3. Create executable source code.
4. Create automated tests.
5. Handle required error cases safely.
6. Create a README explaining the project.
7. Do not merely describe code in your response.
8. Actually write the files into the project root.
9. Do not modify unrelated projects.
10. Do not write anything outside {project_root}.

If files already exist inside {project_root}, inspect them
and improve them instead of creating duplicate files.

After writing the files, briefly report which files
you created or modified.
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Developer"
    ].run(prompt)

    return {
        "implementation": result
    }


# ============================================================
# DATABASE ENGINEER
# ============================================================

def database_engineer_node(state: EngineeringState):

    requirement = state["requirement"]
    architecture = state["architecture"]
    project_root = state["project_root"]

    prompt = f"""
You are the Database Engineer of an autonomous
software engineering squad.

User requirement:
{requirement}

Architecture:
{architecture}

Project root:
{project_root}

Determine whether the application requires a database.

If a database is NOT required, clearly state:

NO DATABASE REQUIRED

If a database IS required:

1. Design the schema.
2. Identify tables.
3. Identify fields.
4. Identify relationships.
5. Explain how the application should use the database.

Do not modify unrelated projects.
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Database Engineer"
    ].run(prompt)

    return {
        "database_design": result
    }


# ============================================================
# TESTER
# ============================================================

def tester_node(state: EngineeringState):

    requirement = state["requirement"]
    architecture = state["architecture"]
    implementation = state["implementation"]
    project_root = state["project_root"]

    prompt = f"""
You are the Tester of an autonomous software engineering
squad.

User requirement:
{requirement}

Architecture:
{architecture}

Developer report:
{implementation}

============================================================
CURRENT PROJECT ROOT
============================================================

{project_root}

============================================================

YOUR TASK
============================================================

Test the ACTUAL generated project.

IMPORTANT:

The project for this run exists ONLY inside:

{project_root}

Do NOT inspect or test unrelated projects.

First inspect the files inside the project root.

Identify the actual project structure.

Then run the appropriate automated tests.

Run commands from the project root when necessary.

For example, if the project contains:

{project_root}/tests/test_calculator.py

you should test that project from:

{project_root}

Use the existing testing framework when available.

Do NOT modify source code.

Do NOT create fake test results.

Do NOT fail because the program expects interactive
stdin. Test the underlying functionality using the
automated test suite.

Your final response MUST end with EXACTLY ONE of:

STATUS: PASS

or

STATUS: FAIL

If tests fail, clearly explain:

1. Which tests failed
2. The error
3. The likely cause
4. What the Developer/Debugger should fix

If all required tests pass, clearly state the
successful test results before:

STATUS: PASS
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Tester"
    ].run(prompt)

    # Explicit status detection.
    normalized = result.upper()

    if "STATUS: PASS" in normalized:
        status = "PASS"
    elif "STATUS: FAIL" in normalized:
        status = "FAIL"
    else:
        status = "FAIL"

    return {
        "test_report": result,
        "test_status": status,
    }


# ============================================================
# DEBUGGER
# ============================================================

def debugger_node(state: EngineeringState):

    requirement = state["requirement"]
    architecture = state["architecture"]
    implementation = state["implementation"]
    test_report = state["test_report"]
    project_root = state["project_root"]

    prompt = f"""
You are the Debugger of an autonomous software
engineering squad.

User requirement:
{requirement}

Architecture:
{architecture}

Developer report:
{implementation}

Tester report:
{test_report}

============================================================
CURRENT PROJECT ROOT
============================================================

{project_root}

============================================================

YOUR TASK
============================================================

Fix the ACTUAL project files causing the test failures.

The project exists ONLY inside:

{project_root}

Inspect the files there using read_project_file.

Run relevant commands/tests using run_project_command.

Identify the root cause.

Then modify the necessary files using
write_project_file.

Do NOT modify unrelated projects.

Do NOT only explain the fix.

Actually fix the code.

After fixing the problem, briefly report:

1. Root cause
2. Files changed
3. Fix applied
4. Tests that should be rerun
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Debugger"
    ].run(prompt)

    return {
        "debugging_report": result,
        "debug_count": state["debug_count"] + 1,
    }


# ============================================================
# CODE REVIEWER
# ============================================================

def code_reviewer_node(state: EngineeringState):

    requirement = state["requirement"]
    architecture = state["architecture"]
    implementation = state["implementation"]
    test_report = state["test_report"]
    debugging_report = state["debugging_report"]
    project_root = state["project_root"]

    prompt = f"""
You are the Code Reviewer of an autonomous software
engineering squad.

User requirement:
{requirement}

Architecture:
{architecture}

Implementation report:
{implementation}

Test report:
{test_report}

Debugging report:
{debugging_report}

Project root:
{project_root}

Review the completed software engineering work.

Check:

1. Requirement coverage
2. Code quality
3. Project structure
4. Error handling
5. Automated tests
6. Maintainability
7. Documentation

If the implementation satisfies the requirement,
approve it.

If there are minor improvements, mention them without
blocking an otherwise working implementation.

Provide a concise final code review.
"""

    result = SOFTWARE_ENGINEERING_SQUAD[
        "Code Reviewer"
    ].run(prompt)

    # Capture ONLY the current project's files.
    generated_files = collect_generated_files(
        project_root
    )

    return {
        "review": result,
        "generated_files": generated_files,
    }


# ============================================================
# ROUTING
# ============================================================

def test_router(state: EngineeringState):

    if state["test_status"] == "PASS":
        return "code_reviewer"

    if state["debug_count"] >= 3:
        return "code_reviewer"

    return "debugger"


# ============================================================
# GRAPH
# ============================================================

builder = StateGraph(EngineeringState)

builder.add_node(
    "project_manager",
    project_manager_node,
)

builder.add_node(
    "architect",
    architect_node,
)

builder.add_node(
    "developer",
    developer_node,
)

builder.add_node(
    "database_engineer",
    database_engineer_node,
)

builder.add_node(
    "tester",
    tester_node,
)

builder.add_node(
    "debugger",
    debugger_node,
)

builder.add_node(
    "code_reviewer",
    code_reviewer_node,
)


# ============================================================
# FLOW
# ============================================================

builder.add_edge(
    START,
    "project_manager",
)

builder.add_edge(
    "project_manager",
    "architect",
)

builder.add_edge(
    "architect",
    "developer",
)

builder.add_edge(
    "developer",
    "database_engineer",
)

builder.add_edge(
    "database_engineer",
    "tester",
)

builder.add_conditional_edges(
    "tester",
    test_router,
    {
        "debugger": "debugger",
        "code_reviewer": "code_reviewer",
    },
)

builder.add_edge(
    "debugger",
    "developer",
)

builder.add_edge(
    "code_reviewer",
    END,
)


engineering_graph = builder.compile()