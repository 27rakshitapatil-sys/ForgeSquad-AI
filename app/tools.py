from pathlib import Path
from datetime import datetime
import re
import subprocess


# =========================================================
# SETTINGS
# =========================================================

# Max characters returned to the model from any tool.
# Tool output is resent to Gemini on every later tool round,
# so keeping it short directly reduces token usage.
MAX_FILE_CHARS = 8000
MAX_COMMAND_HEAD_CHARS = 1500
MAX_COMMAND_TAIL_CHARS = 3500

COMMAND_TIMEOUT_SECONDS = 120


# =========================================================
# EXISTING TOOLS
# =========================================================

def calculator(expression: str) -> str:
    """Evaluate a simple math expression like '12 * (3 + 4)'."""
    allowed = set("0123456789+-*/(). ")

    if not set(expression) <= allowed:
        return "Error: only numbers and + - * / ( ) are allowed."

    try:
        return str(eval(expression))
    except Exception as e:
        return f"Error: {e}"


def get_time() -> str:
    """Return the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# =========================================================
# FORGESQUAD ENGINEERING TOOLS
# =========================================================

PROJECT_ROOT = Path.cwd().resolve()

# Generated projects live in their own folder so agents cannot
# overwrite ForgeSquad's own main.py, README.md, requirements.txt, etc.
# Set WORKSPACE_DIR = PROJECT_ROOT to restore the old behavior.
WORKSPACE_DIR = PROJECT_ROOT / "workspace"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)


def _truncate_middle(text: str, head: int, tail: int) -> str:
    """Keep the start and end of long text (errors are usually at the end)."""
    if len(text) <= head + tail:
        return text

    omitted = len(text) - head - tail
    return (
        text[:head]
        + f"\n\n[... {omitted} characters omitted ...]\n\n"
        + text[-tail:]
    )


def _resolve_inside_workspace(path: str):
    """Resolve a path and make sure it stays inside the workspace."""
    requested_path = (WORKSPACE_DIR / path).resolve()

    if not requested_path.is_relative_to(WORKSPACE_DIR):
        return None

    return requested_path


# =========================================================
# READ PROJECT FILE
# =========================================================

def read_project_file(path: str) -> str:
    """
    Safely read a text file inside the project workspace.

    Paths are relative to the workspace folder.
    The tool prevents access to files outside the workspace.
    """

    try:
        requested_path = _resolve_inside_workspace(path)

        if requested_path is None:
            return "Error: access outside the project workspace is not allowed."

        if not requested_path.exists():
            return f"Error: file not found: {path}"

        if not requested_path.is_file():
            return f"Error: path is not a file: {path}"

        content = requested_path.read_text(
            encoding="utf-8",
            errors="replace",
        )

        if len(content) > MAX_FILE_CHARS:
            omitted = len(content) - MAX_FILE_CHARS
            content = (
                content[:MAX_FILE_CHARS]
                + f"\n\n[... file truncated, {omitted} more characters ...]"
            )

        return content

    except Exception as e:
        return f"Error reading file: {e}"


# =========================================================
# WRITE PROJECT FILE
# =========================================================

def write_project_file(path: str, content: str) -> str:
    """
    Safely create or update a text file inside the project workspace.

    Paths are relative to the workspace folder.
    The tool prevents writing files outside the workspace.
    """

    try:
        requested_path = _resolve_inside_workspace(path)

        if requested_path is None:
            return "Error: access outside the project workspace is not allowed."

        requested_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        requested_path.write_text(
            content,
            encoding="utf-8",
        )

        return f"File written successfully: {path}"

    except Exception as e:
        return f"Error writing file: {e}"


# =========================================================
# RUN PROJECT COMMAND
# =========================================================

# Blocked if they appear as a standalone command word anywhere
# in the command (not only at the start).
_BLOCKED_PATTERN = re.compile(
    r"(^|[;&|`(\s])"
    r"(format|del|erase|rmdir|rd|rm|sudo|chmod|chown|diskpart|"
    r"shutdown|restart-computer|remove-item)"
    r"(\s|/|$)",
    re.IGNORECASE,
)


def run_project_command(command: str) -> str:
    """
    Safely run a development/test command inside the project workspace.

    This tool is intended for software engineering tasks such as:
    - Running tests (for example: python -m pytest)
    - Checking Python files
    - Running project scripts
    - Inspecting command output

    Commands are executed from the workspace folder.
    Interactive input is not available; scripts that call input() will
    receive end-of-input immediately.
    """

    try:
        if not command or not command.strip():
            return "Error: command cannot be empty."

        command = command.strip()

        if _BLOCKED_PATTERN.search(command):
            return (
                "Error: this command is not allowed "
                "by the ForgeSquad project tool."
            )

        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdin=subprocess.DEVNULL,   # prevents hanging on input()
            timeout=COMMAND_TIMEOUT_SECONDS,
        )

        output = ""

        if result.stdout:
            output += "STDOUT:\n"
            output += result.stdout

        if result.stderr:
            output += "\nSTDERR:\n"
            output += result.stderr

        output = _truncate_middle(
            output,
            MAX_COMMAND_HEAD_CHARS,
            MAX_COMMAND_TAIL_CHARS,
        )

        output += f"\n\nEXIT CODE: {result.returncode}"

        if result.returncode == 0:
            output += "\nSTATUS: SUCCESS"
        else:
            output += "\nSTATUS: FAILED"

        return output

    except subprocess.TimeoutExpired:
        return f"Error: command timed out after {COMMAND_TIMEOUT_SECONDS} seconds."

    except Exception as e:
        return f"Error running command: {e}"