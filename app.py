import streamlit as st
from datetime import datetime
import os
from reflexion_agent import ReflexionCodeAgent as ReflexionAgent

# ------------------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------------------
st.set_page_config(
    page_title="Reflexion Code Agent",
    page_icon="◌",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------
# VISUAL SYSTEM
# Two main design colours only:
#   Paper = cool neutral
#   Ink   = deep blue-charcoal
# No gradients, purple, green, or bright blue accents.
# Everything else is derived from these two colours.
# ------------------------------------------------------------
PAPER = "#F5F6F7"
INK = "#202B36"

st.markdown(
    f"""
    <style>
    /* ---------- Global ---------- */
    :root {{
        --paper: {PAPER};
        --ink: {INK};
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {{
        background: var(--paper) !important;
    }}

    [data-testid="stHeader"] {{
        background: var(--paper) !important;
    }}

    /* Remove the Streamlit sidebar completely */
    [data-testid="stSidebar"] {{
        display: none !important;
    }}

    /* Remove the sidebar collapse rail */
    [data-testid="collapsedControl"] {{
        display: none !important;
    }}

    /* Hide Streamlit chrome that makes the page feel like a template */
    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    [data-testid="stToolbar"] {{
        visibility: hidden;
    }}

    /* Main page width */
    .block-container {{
        max-width: 1180px !important;
        padding-top: 28px !important;
        padding-bottom: 70px !important;
        padding-left: 44px !important;
        padding-right: 44px !important;
    }}

    /* ---------- Typography ---------- */
    html, body, [class*="css"] {{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
                     BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    h1, h2, h3, h4, h5, h6, p, label, span, div {{
        color: var(--ink);
    }}

    /* ---------- Top navigation ---------- */
    .brand-row {{
        display: flex;
        align-items: center;
        min-height: 44px;
        padding: 0;
        width: 100%;
        overflow: visible !important;
    }}

    .brand-row * {{
        overflow: visible !important;
    }}

    .top-rule {{
        height: 1px;
        width: 100%;
        background: rgba(32, 43, 54, 0.16);
        margin: 14px 0 62px 0;
    }}

    .header-row {{
        overflow: visible !important;
        min-height: 46px;
    }}

    .header-row [data-testid="stColumn"] {{
        overflow: visible !important;
    }}

    .brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .brand-mark {{
        width: 32px;
        height: 32px;
        border: 1.5px solid var(--ink);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 17px;
        line-height: 1;
    }}

    .brand-name {{
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.02em;
    }}

    .brand-sub {{
        font-size: 12px;
        opacity: 0.62;
        margin-left: 4px;
    }}

    .status-dot {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        opacity: 0.72;
        letter-spacing: 0.03em;
    }}

    .status-dot::before {{
        content: "";
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: var(--ink);
        display: inline-block;
    }}

    /* ---------- Hero ---------- */
    .hero {{
        width: 100%;
        max-width: 900px;
        margin: 0 auto 50px auto;
        text-align: center !important;
        display: flex;
        flex-direction: column;
        align-items: center;
    }}

    .eyebrow {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.20em;
        font-weight: 700;
        opacity: 0.62;
        margin-bottom: 18px;
    }}

    .hero-title {{
        font-family: Georgia, "Times New Roman", serif;
        font-size: clamp(42px, 6vw, 68px);
        line-height: 0.98;
        letter-spacing: -0.045em;
        font-weight: 500;
        margin: 0;
    }}

    .hero-title em {{
        font-style: italic;
    }}

    .hero-copy {{
        width: 100%;
        max-width: 620px;
        margin: 22px auto 0 auto !important;
        font-size: 15px;
        line-height: 1.75;
        opacity: 0.72;
        text-align: center !important;
    }}

    /* ---------- Prompt area ---------- */
    .prompt-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-weight: 700;
        margin-bottom: 10px;
        opacity: 0.72;
    }}

    [data-testid="stTextArea"] textarea {{
        background: rgba(255, 255, 255, 0.34) !important;
        color: var(--ink) !important;
        border: 1px solid rgba(36, 52, 71, 0.28) !important;
        border-radius: 14px !important;
        padding: 18px !important;
        font-size: 15px !important;
        line-height: 1.6 !important;
        box-shadow: none !important;
    }}

    [data-testid="stTextArea"] textarea:focus {{
        border-color: var(--ink) !important;
        box-shadow: 0 0 0 1px var(--ink) !important;
    }}

    [data-testid="stTextArea"] label {{
        display: none !important;
    }}

    /* ---------- Buttons ---------- */
    .stButton > button,
    .stDownloadButton > button {{
        color: var(--ink) !important;
        background: transparent !important;
        border: 1px solid rgba(36, 52, 71, 0.30) !important;
        border-radius: 999px !important;
        min-height: 42px !important;
        padding: 7px 17px !important;
        font-weight: 600 !important;
        box-shadow: none !important;
        transition: all 0.16s ease;
    }}

    .stButton > button,
    .stButton > button *,
    .stDownloadButton > button,
    .stDownloadButton > button * {{
        color: var(--ink) !important;
    }}

    .stButton > button:hover,
    .stButton > button:hover *,
    .stDownloadButton > button:hover,
    .stDownloadButton > button:hover * {{
        background: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
    }}

    /* Main action button */
    .generate-wrap .stButton > button {{
        width: 100% !important;
        min-height: 52px !important;
        border-radius: 12px !important;
        background: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
        font-size: 14px !important;
        letter-spacing: 0.01em;
    }}

    .generate-wrap .stButton > button:hover,
    .generate-wrap .stButton > button:hover * {{
        background: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
        opacity: 0.90;
    }}

    /* Quick examples */
    .examples-title {{
        margin-top: 28px;
        margin-bottom: 11px;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.16em;
        font-weight: 700;
        opacity: 0.60;
    }}

    .example-row .stButton > button,
    .example-row .stButton > button * {{
        width: 100% !important;
        min-height: 38px !important;
        font-size: 12px !important;
        padding: 5px 12px !important;
    }}

    /* ---------- Settings popover ---------- */
    [data-testid="stPopover"] > button {{
        width: 100% !important;
        border: 1px solid rgba(36, 52, 71, 0.25) !important;
        background: transparent !important;
        color: var(--ink) !important;
        border-radius: 999px !important;
        padding: 6px 10px !important;
        min-height: 34px !important;
        font-size: 12px !important;
        white-space: nowrap !important;
    }}

    [data-testid="stPopover"] > button,
    [data-testid="stPopover"] > button * {{
        color: var(--ink) !important;
    }}

    [data-testid="stPopover"] > button:hover,
    [data-testid="stPopover"] > button:hover * {{
        background: var(--ink) !important;
        color: var(--paper) !important;
        border-color: var(--ink) !important;
    }}

    /* Selectbox / slider / number input */
    [data-baseweb="select"] > div,
    [data-testid="stNumberInput"] input {{
        background: rgba(255,255,255,0.30) !important;
        border-color: rgba(36,52,71,0.25) !important;
        color: var(--ink) !important;
    }}

    [data-testid="stSlider"] [role="slider"] {{
        background: var(--ink) !important;
    }}

    /* ---------- Result header ---------- */
    .result-rule {{
        height: 1px;
        background: rgba(36, 52, 71, 0.18);
        margin: 54px 0 32px 0;
    }}

    .result-meta {{
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 18px;
    }}

    .result-title {{
        font-family: Georgia, "Times New Roman", serif;
        font-size: 31px;
        letter-spacing: -0.025em;
        font-weight: 500;
    }}

    .result-detail {{
        font-size: 12px;
        opacity: 0.65;
        white-space: nowrap;
    }}

    .success-line {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        margin-bottom: 20px;
        opacity: 0.78;
    }}

    .success-line::before {{
        content: "";
        width: 8px;
        height: 8px;
        background: var(--ink);
        border-radius: 50%;
    }}

    /* ---------- Code + output panels ---------- */
    .panel-label {{
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.17em;
        font-weight: 700;
        opacity: 0.62;
        margin-bottom: 9px;
    }}

    [data-testid="stCodeBlock"] {{
        border: 1px solid rgba(36, 52, 71, 0.20) !important;
        border-radius: 13px !important;
        overflow: hidden !important;
        background: rgba(255,255,255,0.26) !important;
    }}

    [data-testid="stCodeBlock"] pre {{
        background: transparent !important;
        color: var(--ink) !important;
    }}

    [data-testid="stCodeBlock"] code {{
        color: var(--ink) !important;
    }}

    /* ---------- Expanders ---------- */
    [data-testid="stExpander"] {{
        border: 1px solid rgba(36, 52, 71, 0.20) !important;
        border-radius: 13px !important;
        background: rgba(255,255,255,0.18) !important;
    }}

    [data-testid="stExpander"] summary {{
        color: var(--ink) !important;
    }}

    /* ---------- Checkbox ---------- */
    [data-testid="stCheckbox"] label {{
        color: var(--ink) !important;
        font-size: 12px !important;
    }}

    /* ---------- Status messages ---------- */
    [data-testid="stAlert"] {{
        background: rgba(36, 52, 71, 0.09) !important;
        color: var(--ink) !important;
        border: 1px solid rgba(36, 52, 71, 0.18) !important;
        border-radius: 12px !important;
    }}

    /* ---------- Footer ---------- */
    .footer {{
        text-align: center;
        margin-top: 64px;
        padding-top: 20px;
        border-top: 1px solid rgba(36, 52, 71, 0.14);
        font-size: 11px;
        opacity: 0.52;
    }}

    /* ---------- Mobile ---------- */
    @media (max-width: 760px) {{
        .block-container {{
            padding-left: 20px !important;
            padding-right: 20px !important;
        }}

        .brand-row {{
            margin-bottom: 42px;
        }}

        .hero-title {{
            font-size: 43px;
        }}

        .result-meta {{
            display: block;
        }}

        .result-detail {{
            display: block;
            margin-top: 6px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------
for key in ["result", "runs", "successes", "task"]:
    if key not in st.session_state:
        st.session_state[key] = "" if key == "task" else 0 if key != "result" else None

# ------------------------------------------------------------
# EXAMPLES
# ------------------------------------------------------------
EXAMPLES = [
    ("Factorial", "Write Python code to calculate factorial of 7 and print the result."),
    ("Fibonacci", "Write Python code to print the first 10 Fibonacci numbers."),
    ("Sort a list", "Sort the list [5,2,9,1] and print it."),
    ("Prime numbers", "Generate 100 random ints 1–1000, filter primes, print top 10."),
]

# ------------------------------------------------------------
# TOP BAR
# ------------------------------------------------------------
st.markdown('<div class="header-row">', unsafe_allow_html=True)
top_left, top_right = st.columns([8.5, 1.5], vertical_alignment="center")

with top_left:
    st.markdown(
        """
        <div class="brand-row">
            <div class="brand">
                <div class="brand-mark">◌</div>
                <div>
                    <span class="brand-name">REFLEXION</span>
                    <span class="brand-sub">code agent</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_right:
    with st.popover("Settings"):
        st.markdown("### Agent settings")

        if os.getenv("GROQ_API_KEY"):
            st.caption("API key loaded")
        else:
            st.error("API key missing — add it to .env")

        model = st.selectbox(
            "Model",
            ["openai/gpt-oss-20b", "openai/gpt-oss-120b"],
        )

        max_iters = st.slider("Maximum iterations", 1, 10, 5)
        temperature = st.number_input(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.0,
            step=0.05,
        )

        runs = st.session_state["runs"]
        succ = st.session_state["successes"]
        rate = (succ / runs * 100) if runs else 0

        st.divider()
        st.caption(f"{runs} runs · {succ} successful · {rate:.0f}% success")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="top-rule"></div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# HERO
# ------------------------------------------------------------
st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Generate · Execute · Reflect · Repair</div>
        <h1 class="hero-title">Give it a task.<br><em>Let it figure out the code.</em></h1>
        <p class="hero-copy">
            Reflexion Code Agent writes Python, runs it in a real environment,
            reads the execution feedback, and iterates when something fails.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------
# TASK INPUT
# ------------------------------------------------------------
st.markdown('<div class="prompt-label">Your task</div>', unsafe_allow_html=True)

task = st.text_area(
    "Task description",
    value=st.session_state["task"],
    height=142,
    placeholder="e.g. Read a CSV file, calculate the average of a column, and print the result.",
    label_visibility="collapsed",
)

st.markdown('<div class="generate-wrap">', unsafe_allow_html=True)
if st.button("Generate & Run  →", use_container_width=True):
    st.session_state["task"] = task

    if not task.strip():
        st.warning("Describe a coding task first.")
    else:
        with st.spinner("Agent is working through the task..."):
            agent = ReflexionAgent(
                model=model,
                max_iterations=max_iters,
                temperature=temperature,
            )

            try:
                result = agent.generate_code(task)
            except Exception:
                result = agent.generate(task)

            st.session_state["result"] = result
            st.session_state["runs"] += 1

            if result.get("success"):
                st.session_state["successes"] += 1

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------
# EXAMPLES
# ------------------------------------------------------------
st.markdown('<div class="examples-title">Try a task</div>', unsafe_allow_html=True)

example_cols = st.columns(len(EXAMPLES))
for col, (title, prompt) in zip(example_cols, EXAMPLES):
    with col:
        if st.button(title, key=f"example_{title}", use_container_width=True):
            st.session_state["task"] = prompt
            st.rerun()

# ------------------------------------------------------------
# RESULTS
# ------------------------------------------------------------
result = st.session_state.get("result")

if result:
    st.markdown('<div class="result-rule"></div>', unsafe_allow_html=True)

    success = result.get("success")
    iterations = result.get("iterations", 0)
    code = result.get("code", "")
    history = result.get("history", [])

    status_text = "Execution successful" if success else "Maximum iterations reached"

    st.markdown(
        f"""
        <div class="result-meta">
            <div class="result-title">Agent result</div>
            <div class="result-detail">{iterations} iteration{"s" if iterations != 1 else ""}</div>
        </div>
        <div class="success-line">{status_text}</div>
        """,
        unsafe_allow_html=True,
    )

    if code:
        left, right = st.columns(2, gap="large")

        with left:
            st.markdown('<div class="panel-label">Generated Python</div>', unsafe_allow_html=True)
            st.code(code, language="python", line_numbers=True)

            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = (
                "# Generated by Reflexion Code Agent\n"
                f"# Task: {st.session_state['task']}\n"
                f"# Time: {ts}\n"
                f"# Iterations: {iterations}\n\n"
            )

            st.download_button(
                "Export Python file",
                header + code,
                "generated_with_comments.py",
                use_container_width=True,
            )

        with right:
            st.markdown('<div class="panel-label">Execution output</div>', unsafe_allow_html=True)

            exec_msgs = [m for m in history if m.get("role") == "executor"]

            if exec_msgs:
                last = exec_msgs[-1].get("content", "")
                lines = last.splitlines()

                stdout_lines = []
                stderr_lines = []
                section = None

                for line in lines:
                    if line.startswith("STDOUT:"):
                        section = "stdout"
                        continue
                    if line.startswith("STDERR:"):
                        section = "stderr"
                        continue
                    if line.startswith("Iteration ") or line.startswith("ExitCode="):
                        continue

                    if section == "stdout":
                        stdout_lines.append(line)
                    elif section == "stderr":
                        stderr_lines.append(line)

                clean_stdout = "\n".join(stdout_lines).strip()
                clean_stderr = "\n".join(stderr_lines).strip()

                if clean_stdout:
                    st.code(clean_stdout, language="text")
                elif clean_stderr:
                    st.code(clean_stderr, language="text")
                else:
                    st.caption("The code ran successfully with no printed output.")

                with st.expander("Execution details"):
                    st.code(last, language="text")
            else:
                st.caption("No execution output returned.")

    # --------------------------------------------------------
    # REFLEXION TRACE
    # --------------------------------------------------------
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="panel-label">Reflexion trace</div>', unsafe_allow_html=True)

    trace_lines = []

    for msg in history:
        role = msg.get("role", "")

        if role == "assistant":
            if not trace_lines or trace_lines[-1] != "Code generated":
                trace_lines.append("Code generated")

        elif role == "executor":
            content = msg.get("content", "")
            if "ExitCode=0" in content:
                trace_lines.append("Execution passed")
            else:
                trace_lines.append("Execution failed — feedback returned to agent")

    if not trace_lines:
        trace_lines.append("No trace available")

    trace_html = "".join(
        f'<div style="padding:6px 0; font-size:13px;">'
        f'<span style="display:inline-block;width:7px;height:7px;border-radius:50%;'
        f'background:{INK};margin-right:10px;"></span>{line}</div>'
        for line in trace_lines
    )

    st.markdown(trace_html, unsafe_allow_html=True)

    # --------------------------------------------------------
    # FULL DEBUG HISTORY
    # --------------------------------------------------------
    with st.expander("View full debugging history"):
        for i, msg in enumerate(history, 1):
            role = msg.get("role", "unknown").title()
            st.markdown(f"**Step {i} · {role}**")
            st.code(msg.get("content", ""), language="text")

# ------------------------------------------------------------
# FOOTER
# ------------------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Reflexion Code Agent · Python · Groq
    </div>
    """,
    unsafe_allow_html=True,
)
