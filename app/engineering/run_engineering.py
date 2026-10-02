from datetime import datetime

from app.engineering.engineering_graph import engineering_graph


def run_engineering_project(requirement: str):
    """
    Run the ForgeSquad AI software engineering workflow.
    Each engineering run gets its own isolated project folder.
    """

    # Create a unique project folder for this engineering run.
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    project_root = f"runs/{run_id}"

    initial_state = {
        "requirement": requirement,
        "project_root": project_root,
        "project_plan": "",
        "architecture": "",
        "implementation": "",
        "database_design": "",
        "test_report": "",
        "debugging_report": "",
        "review": "",
        "test_status": "",
        "debug_count": 0,
        "generated_files": {},
    }

    print("\n" + "=" * 70)
    print("FORGESQUAD AI")
    print("AUTONOMOUS SOFTWARE ENGINEERING PLATFORM")
    print("=" * 70)

    print("\nRequirement:")
    print(requirement)

    print("\nProject workspace:")
    print(project_root)

    result = engineering_graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FORGESQUAD AI — FINAL RESULT")
    print("=" * 70)

    print("\nPROJECT PLAN")
    print(result["project_plan"])

    print("\nARCHITECTURE")
    print(result["architecture"])

    print("\nIMPLEMENTATION")
    print(result["implementation"])

    print("\nDATABASE DESIGN")
    print(result["database_design"])

    print("\nTEST REPORT")
    print(result["test_report"])

    print("\nDEBUGGING REPORT")
    print(result["debugging_report"] or "No debugging required.")

    print("\nCODE REVIEW")
    print(result["review"])

    print("\nGENERATED PROJECT FILES")
    generated_files = result.get("generated_files", {})

    if generated_files:
        for file_path in generated_files:
            print(f"  - {file_path}")
    else:
        print("No project files captured.")

    print("\n" + "=" * 70)
    print("FORGESQUAD AI — COMPLETE")
    print("=" * 70)

    return result


if __name__ == "__main__":
    requirement = input(
        "\nEnter the software requirement:\n> "
    ).strip()

    if not requirement:
        print("No requirement provided.")
    else:
        run_engineering_project(requirement)