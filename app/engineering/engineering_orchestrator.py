from app.engineering.software_agents import (
    project_manager,
    architect,
    developer,
    database_engineer,
    tester,
    debugger,
    code_reviewer,
)


class EngineeringOrchestrator:
    """
    Coordinates the ForgeSquad AI software engineering agents.

    Current workflow:

    Project Manager
          ↓
       Architect
          ↓
    Developer
          ↓
    Database Engineer
          ↓
       Tester
          ↓
    Code Reviewer

    If problems are identified:
          ↓
       Debugger
          ↓
       Tester
    """

    def __init__(self):
        self.project_manager = project_manager
        self.architect = architect
        self.developer = developer
        self.database_engineer = database_engineer
        self.tester = tester
        self.debugger = debugger
        self.code_reviewer = code_reviewer

    def run(self, requirement: str) -> dict:
        """
        Run the software engineering squad for a requirement.
        """

        print("\n" + "=" * 60)
        print("FORGESQUAD AI — SOFTWARE ENGINEERING SQUAD")
        print("=" * 60)

        # =====================================================
        # 1. PROJECT MANAGER
        # =====================================================

        print("\n[1/7] Project Manager")
        project_plan = self.project_manager.run(
            f"""
User software requirement:

{requirement}

Create a practical engineering plan for this requirement.
"""
        )

        # =====================================================
        # 2. ARCHITECT
        # =====================================================

        print("\n[2/7] Architect")
        architecture = self.architect.run(
            f"""
User requirement:

{requirement}

Project Manager plan:

{project_plan}

Design the software architecture based on this requirement and plan.
"""
        )

        # =====================================================
        # 3. DEVELOPER
        # =====================================================

        print("\n[3/7] Developer")
        implementation = self.developer.run(
            f"""
User requirement:

{requirement}

Project Manager plan:

{project_plan}

Software architecture:

{architecture}

Prepare the implementation required for this project.
"""
        )

        # =====================================================
        # 4. DATABASE ENGINEER
        # =====================================================

        print("\n[4/7] Database Engineer")
        database_design = self.database_engineer.run(
            f"""
User requirement:

{requirement}

Architecture:

{architecture}

Developer implementation plan:

{implementation}

Design the database requirements for this project.
"""
        )

        # =====================================================
        # 5. TESTER
        # =====================================================

        print("\n[5/7] Tester")
        test_report = self.tester.run(
            f"""
User requirement:

{requirement}

Architecture:

{architecture}

Implementation:

{implementation}

Database design:

{database_design}

Create a testing strategy and identify potential failures.
"""
        )

        # =====================================================
        # 6. DEBUGGER
        # =====================================================

        print("\n[6/7] Debugger")

        debugger_context = f"""
User requirement:

{requirement}

Implementation:

{implementation}

Tester report:

{test_report}

Analyze the testing results.

If there are potential problems, identify their root causes
and propose targeted fixes.

If no problems are identified, clearly state that no debugging
changes are currently required.
"""

        debugging_report = self.debugger.run(debugger_context)

        # =====================================================
        # 7. CODE REVIEWER
        # =====================================================

        print("\n[7/7] Code Reviewer")

        review = self.code_reviewer.run(
            f"""
User requirement:

{requirement}

Architecture:

{architecture}

Implementation:

{implementation}

Database design:

{database_design}

Testing report:

{test_report}

Debugging report:

{debugging_report}

Perform a final software engineering code review.
"""
        )

        print("\n" + "=" * 60)
        print("FORGESQUAD AI — ENGINEERING ANALYSIS COMPLETE")
        print("=" * 60)

        return {
            "requirement": requirement,
            "project_plan": project_plan,
            "architecture": architecture,
            "implementation": implementation,
            "database_design": database_design,
            "test_report": test_report,
            "debugging_report": debugging_report,
            "review": review,
        }