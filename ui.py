import uuid
import streamlit as st
from langgraph.types import Command
from app.graph import graph
from app.memory import save_run, find_related

st.set_page_config(page_title="Agent Orchestration System", page_icon="🤖")
st.title("🤖 Agent Orchestration System")

# Keep one thread id per browser session so the graph can pause and resume
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.result = None
    st.session_state.goal = ""

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ---- Start a new run ----
goal = st.text_input("What should the team work on?")

if st.button("Start run") and goal:
    st.session_state.thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": st.session_state.thread_id}}
    st.session_state.goal = goal

    matches = find_related(goal)
    background = "\n\n".join(f"Past goal: {g}\nPast result: {r[:500]}" for g, r in matches)

    with st.spinner("Agents are working..."):
        st.session_state.result = graph.invoke(
            {"goal": goal, "work": "", "next": "", "steps": 0, "background": background},
            config,
        )

result = st.session_state.result

# ---- Show approval request or final result ----
if result:
    if "__interrupt__" in result:
        info = result["__interrupt__"][0].value
        st.warning(info["question"])
        st.markdown(info["work"])
        col1, col2 = st.columns(2)
        decision = None
        if col1.button("✅ Approve"):
            decision = "approve"
        if col2.button("❌ Reject"):
            decision = "reject"
        if decision:
            with st.spinner("Continuing..."):
                st.session_state.result = graph.invoke(Command(resume=decision), config)
            st.rerun()
    else:
        st.success("Run finished")
        st.markdown(result["work"])
        if st.session_state.get("saved_thread") != st.session_state.thread_id:
            save_run(st.session_state.goal, result["work"])
            st.session_state.saved_thread = st.session_state.thread_id