import streamlit as st
from llm_client import call_hf_llm
from prompts import build_student_prompt, explain_prompt_prompt, quest_instruction


st.set_page_config(page_title="Prompt Lab for College Students", layout="wide")

st.title("🎓 Prompt Lab for College Students")
st.caption("Interactive playground to learn prompt engineering with LLMs.")

tab_builder, tab_compare, tab_quests, tab_teacher = st.tabs(
    ["Prompt Builder", "A/B Experiment", "Quests", "Teacher Mode"]
)

# 1) Prompt Builder
with tab_builder:
    st.subheader("Prompt Building Blocks")

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox(
            "Role",
            [
                "AI teaching assistant for an introductory AI course",
                "Data analyst explaining results to a non-technical manager",
                "Academic writing tutor for research reports",
                "UX researcher summarizing interview findings",
            ],
        )
        task = st.text_area(
            "Task",
            "Explain overfitting in machine learning to a first-year CS student.",
            height=80,
        )
        context = st.text_area(
            "Context",
            "Course: Intro to Machine Learning. Student has basic calculus and Python.",
            height=80,
        )

    with col2:
        examples = st.text_area(
            "Examples (optional)",
            "Example: When I say 'keep it simple', avoid equations unless necessary.",
            height=80,
        )
        output_style = st.selectbox(
            "Output style",
            [
                "Short bullet points with a simple analogy",
                "Step-by-step explanation with headings",
                "FAQ style (questions and answers)",
                "Formal paragraph suitable for lecture notes",
            ],
        )

    # initialize session state
    if "last_prompt" not in st.session_state:
        st.session_state.last_prompt = ""
    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""

    # First button: generate answer
    if st.button("Generate Response", type="primary"):
        prompt_text = build_student_prompt(role, task, context, examples, output_style)
        with st.spinner("Asking the model..."):
            answer = call_hf_llm(prompt_text)

        st.session_state.last_prompt = prompt_text
        st.session_state.last_answer = answer

    # Show last result if available
    if st.session_state.last_prompt:
        st.markdown("**Prompt sent to the model:**")
        st.code(st.session_state.last_prompt, language="markdown")
        st.markdown("**Model response:**")
        st.write(st.session_state.last_answer)

        # Second button: explain the prompt
        if st.button("Explain why this prompt worked / how to improve it",type="primary"):
            with st.spinner("Analyzing prompt..."):
                explain_prompt = explain_prompt_prompt(
                    st.session_state.last_prompt,
                    st.session_state.last_answer,
                )
                explanation = call_hf_llm(explain_prompt, max_new_tokens=256)
            st.markdown("**Prompt engineering feedback:**")
            st.write(explanation)


# 2) A/B Experiment
with tab_compare:
    st.subheader("Side-by-Side Prompt Experiment")
    st.caption("Compare two prompts to see how small changes affect the output.")

    colA, colB = st.columns(2)

    with colA:
        st.markdown("**Prompt A**")
        prompt_a = st.text_area(
            "Prompt A",
            "Explain gradient descent.",
            height=120,
            key="prompt_a",
        )
        run_a = st.button("Run A")

    with colB:
        st.markdown("**Prompt B**")
        prompt_b = st.text_area(
            "Prompt B",
            "Explain gradient descent to a first-year CS student using a hill-descent analogy and simple language.",
            height=120,
            key="prompt_b",
        )
        run_b = st.button("Run B")

    col_out_a, col_out_b = st.columns(2)

    if run_a:
        with col_out_a:
            with st.spinner("Running Prompt A..."):
                out_a = call_hf_llm(prompt_a)
            st.markdown("**Output A:**")
            st.write(out_a)

    if run_b:
        with col_out_b:
            with st.spinner("Running Prompt B..."):
                out_b = call_hf_llm(prompt_b)
            st.markdown("**Output B:**")
            st.write(out_b)

# 3) Quests
with tab_quests:
    st.subheader("Guided Quests")
    quest = st.selectbox(
        "Choose a quest",
        [
            "Explain_gradient_descent",
            "Refine_SQL_prompt",
            "Custom_task",
        ],
    )
    st.markdown("**Quest description:**")
    st.write(quest_instruction(quest))

    user_prompt = st.text_area(
        "Your prompt for this quest",
        "Write a prompt here that follows the quest instructions.",
        height=120,
    )

    if st.button("Run quest prompt"):
        with st.spinner("Running your quest prompt..."):
            quest_output = call_hf_llm(user_prompt)
        st.markdown("**Model response:**")
        st.write(quest_output)

        if st.button("Explain why this quest prompt worked / how to improve it"):
            with st.spinner("Analyzing quest prompt..."):
                explain_prompt = explain_prompt_prompt(user_prompt, quest_output)
                explanation = call_hf_llm(explain_prompt, max_new_tokens=256)
            st.markdown("**Prompt engineering feedback:**")
            st.write(explanation)


# 4) Teacher Mode (read-only for now)
with tab_teacher:
    st.subheader("Teacher Mode (Concept Only)")
    st.markdown(
        """
        - Use the Prompt Builder as an in-class demo to show how role, context, and examples change outputs.  
        - Use A/B Experiment for quick labs: students design Prompt A and B and reflect on differences.  
        - Use Quests as graded or ungraded activities in AI / HCI / EdTech courses.
        """
    )
