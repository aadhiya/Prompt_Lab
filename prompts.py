from textwrap import dedent

def build_student_prompt(role, task, context, examples, output_style):
    return dedent(f"""
    You are acting as: {role}.

    Task:
    {task}

    Context:
    {context}

    Examples (if any):
    {examples}

    Output style:
    {output_style}

    Produce a clear, concise response suitable for a university student.
    """)

def explain_prompt_prompt(prompt_text, model_output):
    return dedent(f"""
    You are a tutor teaching prompt engineering to university students.

    Given this prompt:
    ---
    {prompt_text}
    ---

    And this model response:
    ---
    {model_output}
    ---

    Explain in simple terms:
    1) What parts of the prompt worked well.
    2) What is missing or ambiguous.
    3) How to improve the prompt for better, more reliable results.

    Keep it under 200 words.
    """)

def quest_instruction(name):
    if name == "Explain_gradient_descent":
        return ("Design a prompt that gets the model to explain gradient descent "
                "to a first-year CS student with a simple analogy.")
    if name == "Refine_SQL_prompt":
        return ("Start from a vague prompt asking for an SQL query and refine it "
                "step by step to get a correct, well-formatted answer.")
    return "Design a clear, structured prompt for a realistic university task."
