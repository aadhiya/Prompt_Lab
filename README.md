# Prompt_Lab
# Prompt Lab for College Students

An interactive Streamlit app where college students learn **prompt engineering** by building prompts from blocks, running A/B experiments, and getting LLM‑generated feedback on how to improve their prompts.

This acts as a small **simulation environment** for designing and testing LLM‑based tools in education and research (classroom engagement assistants, research summarizers, feedback generators, etc.), directly supporting:

> “Design and develop business cases and simulation using LLMs in educational and research settings, ranging from classroom engagement tools to data‑driven research methodologies.”

---

## Why this app is useful

### Educational & classroom use

- Lets students and instructors **prototype LLM‑powered classroom tools** (explainers, tutors, feedback assistants) without writing complex code.
- Shows how changing **role, task, context, examples, and output style** affects the behavior of an LLM, which is central to prompt engineering in modern AI courses.[web:299]

### Research and data‑driven methodologies

- The **A/B Experiment** tab turns prompt design into an **experiment variable**: Prompt A vs Prompt B with visible outcome differences.
- Researchers can observe how prompt structure impacts clarity, length, hallucination, and alignment with task goals, supporting **data‑driven prompt engineering studies**.[web:300]

### Business cases and simulations

- By comparing prompts, users can reason about:
  - How better prompts improve answer quality and student understanding.
  - How prompt templates could power scalable tools (grading helpers, feedback bots, research summarizers).
- This helps build **business cases** for deploying LLMs in learning and research workflows before investing in full integrations.

---

## Architecture overview

**Tech stack**

- **Frontend**: Streamlit – quick, reactive UI for forms, tabs, and experiments.
- **Backend LLM**: Hugging Face `InferenceClient` calling a **chat‑completion model** via Hugging Face Inference Providers.
- **Configuration**: `.env` file with:
  - `HF_API_TOKEN` – Hugging Face token with Inference permissions.
  - `HF_MODEL_ID` – ID of a supported chat model (e.g. `openai/gpt-oss-120b:fastest`).

**Code modules**

- `app.py`  
  Streamlit app: tabs, inputs, buttons, and layout. Calls `call_hf_llm` and uses helpers from `prompts.py`.

- `llm_client.py`
  Thin wrapper around `huggingface_hub.InferenceClient`:

 # Concatenate message content from choices
 
This keeps all model‑specific details in one place, and later can be swapped for a LangChain `ChatHuggingFace` integration if chains/tools are added.[web:298][web:313]

- `prompts.py`  
Prompt template functions:

- `build_student_prompt(role, task, context, examples, output_style)`  
  Builds a structured prompt from the UI blocks (role, task, etc.).
- `explain_prompt_prompt(prompt_text, model_output)`  
  Creates a meta‑prompt asking the LLM to **analyze and critique** the original prompt.
- `quest_instruction(name)`  
  Returns a short description and hint for each guided quest.

> LangChain is installed to keep the environment ready for future chains, tools, and memory (e.g., multi‑step workflows, RAG over course materials). For this minimal demo, the logic stays in `llm_client.py` to keep the teaching flow simple.[web:298][web:313]

---

## Features and how they map to learning goals

### 1. Prompt Builder

**UI elements**

- Role selector (e.g. “AI teaching assistant for an introductory AI course”).
- Task input (e.g. “Explain overfitting in machine learning to a first‑year CS student.”).
- Context input (course, student background).
- Examples (optional hints like “avoid equations unless necessary”).
- Output style selector (bullets, FAQ, step‑by‑step, etc.).

**Flow**

1. User sets the fields and clicks **“Generate Response”**.
2. `build_student_prompt(...)` creates a single prompt text from these components.
3. `call_hf_llm(prompt_text)` sends a chat completion request to the configured HF model with a `max_tokens` limit.[web:299][web:317]
4. The prompt and model output are stored in `st.session_state.last_prompt` and `st.session_state.last_answer` and displayed.

**Explain button**

- When the user clicks **“Explain why this prompt worked / how to improve it”**, the app:
1. Builds a meta‑prompt with `explain_prompt_prompt(last_prompt, last_answer)`.
2. Calls `call_hf_llm` again to get a short explanation that:
   - Highlights what parts of the prompt worked.
   - Points out missing/ambiguous elements.
   - Suggests an improved prompt.

**Why this matters**

- Students see **how prompt structure affects the LLM**, learning core prompt engineering techniques (role prompting, audience specification, examples, explicit output style).
- This effectively **simulates classroom tools** like AI TAs or explanation bots, and can be used to argue how better prompt design improves learning experiences.

---

### 2. A/B Experiment

**UI elements**

- Two text areas: **Prompt A** and **Prompt B**.
- Two buttons: **Run A**, **Run B**.
- Two output columns: **Output A**, **Output B**.

**Flow**

- Each button triggers a separate `call_hf_llm(prompt)` call, and outputs are rendered side‑by‑side.

**Educational/research use**

- Allows students and researchers to:
- Compare vague vs detailed prompts.
- Test few‑shot vs zero‑shot approaches.
- See the impact of adding constraints or roles.

This tab acts as a **simple experimental lab** where prompts are independent variables and outcomes are the responses. This supports **data‑driven research methodologies** for prompt engineering.

---

### 3. Quests

**UI elements**

- Quest selector (e.g. `Explain_gradient_descent`, `Refine_SQL_prompt`, `Custom_task`).
- Quest description (from `quest_instruction(name)`).
- Text area for the user’s prompt.
- Button: **Run quest prompt**.
- Button: **Explain why this quest prompt worked / how to improve it**.

**Flow**

1. User selects a quest and reads the instructions (e.g. “Design a prompt explaining gradient descent to a first‑year CS student.”).
2. User designs their own prompt and clicks **Run quest prompt**.
3. The LLM output is displayed.
4. Clicking **Explain…** sends a meta‑prompt (again using `explain_prompt_prompt`) to critique and refine the student’s prompt.

**Why this matters**

- Turns prompt engineering into **guided exercises** that can be integrated into homework, labs, or workshops.
- Helps students practice **iterative refinement**, which is crucial when building LLM‑based tools for education and research.

---

### 4. Teacher Mode

Read‑only text explaining:

- How instructors can:
- Demo prompt effects live.
- Turn A/B experiments into small lab assignments.
- Use quests as assessment items in AI / HCI / AI‑in‑Education courses.
- How the tool can be used in **AI outreach workshops** with partner institutions and communities.

This frames the project as not just a toy, but a **teaching/research instrument** for LLM‑based educational innovation.

---

## LLM choice and configuration

The app uses Hugging Face’s **chat completion** API via `InferenceClient`:

- `HF_API_TOKEN` must have **Inference Providers** permissions to call `chat_completion` endpoints.[web:216][web:318]
- `HF_MODEL_ID` is set to a model that HF Inference supports for chat completion (for example `openai/gpt-oss-120b:fastest`, or another supported chat model listed on HF’s Inference Providers page).[web:293][web:299]

Reasons for this setup:

- **Chat models** understand multi‑turn `messages` and are tuned for **instruction following**, perfect for educational prompts and prompt‑feedback tasks.[web:299]
- Using Inference Providers avoids having to self‑host models, making deployment to Streamlit Cloud or similar platforms straightforward.

The model ID is configurable via environment variables so future experiments can compare **different LLMs** (Mistral, LLaMA‑family, etc.) as part of research.

---

## Why some responses are truncated

Sometimes responses end mid‑sentence, especially in the feedback section. Main reasons:

1. **Token limit in the app**  
 - `call_hf_llm` passes `max_tokens` (e.g. 256 or 512) to `chat_completion`, which limits **how many tokens** the model can generate.[web:299][web:314]  
 - If the ideal answer is longer than this, it is **cut off**.

2. **Provider‑side limits**  
 - Some HF Inference plans and models have their own internal output limits for latency and cost reasons.[web:299][web:318]

This is expected for most LLM APIs. Users can:

- Increase `max_tokens` in the code (with higher latency/cost), and/or  
- Keep prompts asking for **short responses** (e.g. “under 200 words”), which the meta‑prompt already encourages.

---

## How to run locally

1. **Clone and create venv**

git clone https://github.com/your-user/prompt-lab-college.git
cd prompt-lab-college
python -m venv .venv
.venv\Scripts\activate # on Windows
pip install -r requirements.txt

2. **Create `.env`**

HF_API_TOKEN=hf_your_token_with_inference_permissions
HF_MODEL_ID=openai/gpt-oss-120b:fastest

3. **Run**
   streamlit run app.py


Open `http://localhost:8501` in your browser.

---

## How this supports “business cases and simulations”

- The app **simulates** how an LLM‑powered assistant would behave in a course:
  - Explaining concepts at different difficulty levels.
  - Providing structured summaries and analogies.
  - Responding to different prompt designs.
- It enables **quick experimentation** with prompts before building full systems, which is exactly what is needed when:
  - Designing new educational tools (tutors, graders, feedback agents).
  - Justifying resource allocation for LLM integration in courses or research workflows.
- It can be used to **collect observations and small datasets** (e.g. rating outputs under different prompts), forming the basis of data‑driven research on LLM behavior in education.

In short, this app is a compact, deployable demo of **LLM‑based educational innovation**, showing both **prompt engineering concepts** and a realistic **simulation environment** for classroom and research use.

  

