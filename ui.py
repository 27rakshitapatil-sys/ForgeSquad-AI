import io
import zipfile

import streamlit as st

from app.engineering.run_engineering import run_engineering_project


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ForgeSquad AI",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 ForgeSquad AI")

st.subheader(
    "Autonomous Multi-Agent Software Engineering Platform"
)

st.write(
    "Describe the software you want to build. "
    "ForgeSquad AI will plan, design, implement, test, debug, "
    "and review the project using autonomous AI agents."
)

st.divider()


# ============================================================
# REQUIREMENT INPUT
# ============================================================

st.markdown("### 📝 Software Requirement")

requirement = st.text_area(
    "What do you want ForgeSquad AI to build?",
    placeholder=(
        "Example: Build a Python calculator with addition, "
        "subtraction, multiplication, and division. "
        "Division by zero should show a clear error."
    ),
    height=150,
)


# ============================================================
# START ENGINEERING
# ============================================================

if st.button(
    "🚀 Start Engineering",
    type="primary",
):

    if not requirement.strip():

        st.warning(
            "Please enter a software requirement first."
        )

    else:

        st.session_state["engineering_result"] = None

        with st.spinner(
            "ForgeSquad AI agents are working... "
            "This may take a few minutes."
        ):

            try:

                result = run_engineering_project(
                    requirement.strip()
                )

                st.session_state[
                    "engineering_result"
                ] = result

            except Exception as e:

                st.error(
                    "ForgeSquad AI encountered an error."
                )

                st.exception(e)


# ============================================================
# RESULT
# ============================================================

result = st.session_state.get(
    "engineering_result"
)


if result:

    st.success(
        "✅ ForgeSquad AI completed the engineering workflow."
    )

    st.divider()


    # ========================================================
    # PROJECT PLAN
    # ========================================================

    with st.expander(
        "📋 Project Plan",
        expanded=True,
    ):

        st.markdown(
            result.get(
                "project_plan",
                "No project plan available.",
            )
        )


    # ========================================================
    # ARCHITECTURE
    # ========================================================

    with st.expander(
        "🏗️ Architecture"
    ):

        st.markdown(
            result.get(
                "architecture",
                "No architecture available.",
            )
        )


    # ========================================================
    # IMPLEMENTATION REPORT
    # ========================================================

    with st.expander(
        "💻 Implementation Report"
    ):

        st.markdown(
            result.get(
                "implementation",
                "No implementation report available.",
            )
        )


    # ========================================================
    # DATABASE DESIGN
    # ========================================================

    with st.expander(
        "🗄️ Database Design"
    ):

        st.markdown(
            result.get(
                "database_design",
                "No database design available.",
            )
        )


    # ========================================================
    # TEST STATUS
    # ========================================================

    test_status = result.get(
        "test_status",
        "",
    )


    if test_status == "PASS":

        st.success(
            "🧪 Tests Passed"
        )

    elif test_status == "FAIL":

        st.error(
            "🧪 Tests Failed"
        )

    else:

        st.warning(
            "🧪 Test status unavailable."
        )


    # ========================================================
    # TEST REPORT
    # ========================================================

    with st.expander(
        "🧪 Test Report",
        expanded=True,
    ):

        st.markdown(
            result.get(
                "test_report",
                "No test report available.",
            )
        )


    # ========================================================
    # DEBUGGING REPORT
    # ========================================================

    debugging_report = result.get(
        "debugging_report"
    )


    with st.expander(
        "🐛 Debugging Report"
    ):

        if debugging_report:

            st.markdown(
                debugging_report
            )

        else:

            st.info(
                "No debugging was required."
            )


    # ========================================================
    # CODE REVIEW
    # ========================================================

    with st.expander(
        "🔍 Code Review",
        expanded=True,
    ):

        st.markdown(
            result.get(
                "review",
                "No code review available.",
            )
        )


    # ========================================================
    # GENERATED PROJECT
    # ========================================================

    st.divider()

    st.markdown(
        "## 💻 Generated Project"
    )

    st.write(
        "These are the actual files created by the "
        "ForgeSquad AI engineering agents."
    )


    generated_files = result.get(
        "generated_files",
        {}
    )


    if generated_files:

        # ----------------------------------------------------
        # FILE COUNT
        # ----------------------------------------------------

        st.success(
            f"📦 {len(generated_files)} project files generated."
        )


        # ----------------------------------------------------
        # FILE TREE
        # ----------------------------------------------------

        with st.expander(
            "📁 Project Files",
            expanded=True,
        ):

            for file_path in generated_files:

                st.code(
                    file_path,
                    language="text",
                )


        # ----------------------------------------------------
        # FILE VIEWER
        # ----------------------------------------------------

        st.markdown(
            "### 👁️ View Source Code"
        )

        selected_file = st.selectbox(
            "Select a file to view",
            options=list(
                generated_files.keys()
            ),
        )


        if selected_file:

            file_content = generated_files[
                selected_file
            ]


            # Detect a suitable syntax highlighting
            # language from the file extension.

            extension = ""

            if "." in selected_file:

                extension = (
                    selected_file
                    .rsplit(".", 1)[-1]
                    .lower()
                )


            language_map = {

                "py": "python",

                "js": "javascript",

                "jsx": "javascript",

                "ts": "typescript",

                "tsx": "typescript",

                "html": "html",

                "css": "css",

                "json": "json",

                "md": "markdown",

                "txt": "text",

                "yaml": "yaml",

                "yml": "yaml",

                "xml": "xml",

                "sql": "sql",

                "sh": "bash",

                "bat": "bat",

            }


            language = language_map.get(
                extension,
                "text",
            )


            st.caption(
                f"📄 {selected_file}"
            )


            st.code(
                file_content,
                language=language,
            )


        # ----------------------------------------------------
        # DOWNLOAD PROJECT
        # ----------------------------------------------------

        st.markdown(
            "### ⬇️ Download Project"
        )

        zip_buffer = io.BytesIO()


        with zipfile.ZipFile(
            zip_buffer,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
        ) as zip_file:

            for file_path, content in generated_files.items():

                zip_file.writestr(
                    file_path,
                    content,
                )


        zip_buffer.seek(0)


        st.download_button(
            label="⬇️ Download Project ZIP",
            data=zip_buffer.getvalue(),
            file_name="ForgeSquad_generated_project.zip",
            mime="application/zip",
        )


    else:

        st.warning(
            "No generated project files were captured."
        )


    # ========================================================
    # COMPLETION
    # ========================================================

    st.divider()

    st.success(
        "🎉 ForgeSquad AI — Autonomous Engineering Workflow Complete"
    )