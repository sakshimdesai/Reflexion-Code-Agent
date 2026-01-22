import streamlit as st
from datetime import datetime
import os
from reflexion_agent import ReflexionCodeAgent as ReflexionAgent
import json
import html
import uuid

# ------------------------------------
# PAGE CONFIG — Clean white UI
# ------------------------------------
st.set_page_config(page_title="Reflexion Code Agent", page_icon="🤖", layout="wide")

# ------------------------------------
# CLEAN WHITE THEME (minimal UI)
# ------------------------------------
st.markdown(
    """
    <style>

    /* Full-page background: white */
    [data-testid="stAppViewContainer"] {
        background: white !important;
        color: #000000 !important;
    }

    /* Sidebar clean white */
    [data-testid="stSidebar"] {
        background: white !important;
        color: black !important;
        border-right: 1px solid #ececec;
    }

    /* All headings and text */
    h1, h2, h3, h4, h5, h6, p, label, span {
        color: #000000 !important;
    }

    /* Text input and textarea text color */
    textarea, input, .stTextInput>div>div>input {
        color: black !important;
    }

    /* Code blocks */
    .stCodeBlock pre {
        background: #f5f5f5 !important;
        color: #000 !important;
        border-radius: 8px;
        padding: 12px !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* TRANSPARENT BUTTON STYLE */
    .stButton>button, .stDownloadButton>button {
        background: rgba(0,0,0,0.05) !important;
        color: #000 !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        border-radius: 8px !important;
        padding: 8px 14px !important;
        transition: 0.18s ease-in-out;
        font-weight: 500 !important;
    }

    /* Button hover */
    .stButton>button:hover, .stDownloadButton>button:hover {
        background: rgba(0,0,0,0.12) !important;
        border: 1px solid rgba(0,0,0,0.30) !important;
    }

    /* Quick example buttons same size */
    .stColumns .stButton>button {
        min-width: 150px !important;
        padding: 10px 12px !important;
    }

    /* Card-like containers */
    .card-like {
        background: #fafafa;
        padding: 12px;
        border-radius: 10px;
        border: 1px solid #e6e6e6;
    }

    /* Copy button styling */
    .copy-btn button {
        background: rgba(0,0,0,0.05) !important;
        color: black !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        padding: 6px 10px;
        border-radius: 6px;
        cursor: pointer;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------
# Title
# ------------------------------------
st.title("Reflexion Code Agent 🤖")
st.markdown("**AI that writes, tests, and fixes its own code.**")

# ------------------------------------
# Copy-to-Clipboard helper
# ------------------------------------
def render_copy_to_clipboard_button(text_to_copy: str, label: str = "Copy", key: str = None):
    encoded = json.dumps(text_to_copy)
    uid = (key or str(uuid.uuid4())).replace("-", "_")
    html_snippet = f"""
    <div class="copy-btn">
      <button id="btn_{uid}" title="{html.escape(label)}">{html.escape(label)}</button>
      <script>
      const txt_{uid} = {encoded};
      document.getElementById("btn_{uid}").onclick = async function() {{
        await navigator.clipboard.writeText(txt_{uid});
        const b = document.getElementById("btn_{uid}");
        const t = b.innerText;
        b.innerText = "Copied!";
        setTimeout(()=> b.innerText = t, 900);
      }};
      </script>
    </div>
    """
    st.components.v1.html(html_snippet, height=42)

# ------------------------------------
# Session state
# ------------------------------------
for key in ["result", "runs", "successes", "task"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "task" else 0 if key != "result" else None

# ------------------------------------
# Quick example prompts
# ------------------------------------
EXAMPLES = [
    ("Factorial demo", "Write Python code to calculate factorial of 7 and print the result."),
    ("Fibonacci demo", "Write Python code to print the first 10 Fibonacci numbers."),
    ("Sort list demo", "Sort the list [5,2,9,1] and print it."),
    ("Top primes demo", "Generate 100 random ints 1–1000, filter primes, print top 10."),
    ("Scrape Wikipedia (sections)", "Scrape the 'Python (programming language)' page and list first 10 section headings."),
]

# ------------------------------------
# Sidebar
# ------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")

    if os.getenv("GROQ_API_KEY"):
        st.success("API Key Loaded")
    else:
        st.error("API Key Missing — add to .env")

    model = st.selectbox("Select Model", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    max_iters = st.slider("Max Iterations", 1, 10, 5)
    temperature = st.number_input("Temperature", 0.0, 1.0, 0.0, 0.05)

    st.markdown("---")
    st.header("📊 Success Rate Tracker")
    runs = st.session_state["runs"]
    succ = st.session_state["successes"]
    rate = (succ / runs * 100) if runs else 0
    st.write(f"Total runs: {runs}")
    st.write(f"Successful: {succ}")
    st.write(f"Success Rate: **{rate:.1f}%**")
    st.progress(rate / 100 if runs else 0)

# ------------------------------------
# Main Input Section
# ------------------------------------
st.markdown("### Quick Examples")
cols = st.columns(len(EXAMPLES))
for c, (title, prompt) in zip(cols, EXAMPLES):
    if c.button(title):
        st.session_state["task"] = prompt

st.markdown("### Describe the coding task:")
task = st.text_area("Task description", value=st.session_state["task"], height=120)

if st.button("🚀 Generate & Run"):
    st.session_state["task"] = task
    with st.spinner("Agent working..."):
        agent = ReflexionAgent(model=model, max_iterations=max_iters, temperature=temperature)

        try:
            result = agent.generate_code(task)
        except:
            result = agent.generate(task)

        st.session_state["result"] = result
        st.session_state["runs"] += 1
        if result.get("success"):
            st.session_state["successes"] += 1

# ------------------------------------
# Output Section
# ------------------------------------
result = st.session_state.get("result")

if result:
    if result.get("success"):
        st.success(f"Success in {result['iterations']} iteration(s)!")
    else:
        st.error(f"Failed after {result['iterations']} iteration(s).")

    code = result.get("code", "")
    st.markdown("### 📝 Generated Code")

    if code:
        st.markdown('<div class="card-like">', unsafe_allow_html=True)
        st.code(code, language="python")
        st.markdown('</div>', unsafe_allow_html=True)

        render_copy_to_clipboard_button(code, "Copy Code")

        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        header = (
            f"# Generated by Reflexion Agent\n"
            f"# Task: {st.session_state['task']}\n"
            f"# Time: {ts}\n"
            f"# Iterations: {result['iterations']}\n\n"
        )
        st.download_button("💾 Export with comments", header + code, "generated_with_comments.py")

    st.markdown("---")
    st.markdown("### ⚙️ Execution (Debugger)")

    history = result.get("history", [])
    exec_msgs = [m for m in history if m.get("role") == "executor"]

    if exec_msgs:
        last = exec_msgs[-1].get("content", "")
        with st.expander("Executor Output"):
            st.text(last)
            render_copy_to_clipboard_button(last, "Copy Output")

    if st.checkbox("🔍 View Debugging Process"):
        for i, msg in enumerate(history, 1):
            with st.expander(f"{i}. {msg.get('role','')}"):
                st.text(msg.get("content", ""))

# ------------------------------------
# Footer
# ------------------------------------
st.caption("Built with Streamlit • Groq • Reflexion AI 💡")