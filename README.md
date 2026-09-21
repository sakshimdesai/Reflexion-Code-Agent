# Reflexion Code Agent 🤖

A self-correcting AI code generation agent that writes Python code, executes it automatically, detects errors, and fixes them iteratively. 
No copy-paste needed—just describe what you want and watch the agent deliver working code.

## What Problem Does This Solve?

Normally, using AI for code generation is a loop: get code → copy it → run it → hit errors → paste error back → repeat.

**Reflexion Code Agent automates that entire loop.**

| Traditional Workflow | Reflexion Code Agent |
|---|---|
| AI generates code | AI generates + executes code |
| Manual copy-paste | Automatic execution |
| Human debugs errors | AI debugs & fixes errors |
| Multiple round trips | Single-turn solution |


## Key Features

✅ **Natural Language → Working Code** — Describe your task in plain English  
✅ **Automatic Execution** — Generated code runs immediately  
✅ **Self-Correcting Loop** — Errors are captured and fed back to fix the code  
✅ **Real Execution** — Uses Python `subprocess` for genuine execution (not simulated)  
✅ **Full Debug History** — See every iteration and what went wrong  
✅ **Export Options** — Download generated code with metadata  
✅ **Web-Based UI** — No installation needed, runs in browser  

---

## How It Works

### The Reflexion Loop

1. **User Input** — You describe a coding task
2. **Code Generation** — LLM generates Python code in a markdown code block
3. **Execution** — Code runs locally; stdout/stderr are captured
4. **Error Detection** — If exit code ≠ 0, errors are logged
5. **Feedback & Retry** — Error output is sent back to the LLM
6. **Iteration** — Steps 2–5 repeat until code succeeds or max iterations hit

This is **agentic AI**: the model observes its own execution output and adapts its behavior accordingly.

---

## Quick Start



### Local Setup

#### Prerequisites

- Python 3.8+
- Groq API Key ([Get one free](https://console.groq.com))

#### Installation

```bash
# Clone the repo
git clone https://github.com/yourusername/reflexion-code-agent.git
cd reflexion-code-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GROQ_API_KEY=your_groq_api_key_here" > .env

# Run the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Project Structure

```
reflexion-code-agent/
├── app.py                  # Streamlit frontend & UI
├── reflexion_agent.py      # Core agent logic (the brain)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
└── code_workspace/         # Temporary directory for generated code
    └── run_logs/          # Execution logs (stdout/stderr)
```

### `app.py`
The Streamlit web interface. Handles:
- User input and task description
- Model/temperature configuration
- Result visualization and debugging UI
- Code export and copy-to-clipboard functionality

### `reflexion_agent.py`
The core agent that:
- Sends prompts to Groq LLM
- Extracts Python code from model responses
- Executes code using `subprocess.run()`
- Captures execution output and errors
- Implements the reflexion loop (retry logic)

---

## Usage Examples

### Example 1: Simple Algorithm
**Task:** "Write code to find the factorial of 5 and print it"

**Result:** Agent generates, runs, and outputs correct code in 1 iteration.

### Example 2: Data Processing
**Task:** "Read a CSV file, filter rows where age > 30, and save to a new file"

**Result:** Agent generates code, handles missing imports, fixes path issues, and delivers working solution.

### Example 3: API Integration
**Task:** "Fetch JSON from an API and print the top 5 keys"

**Result:** Agent generates proper error handling, retries if needed, and outputs result.

---

## Configuration

### Model Selection
Current default: **LLaMA 3.1 8B Instant** (via Groq)

Available models on Groq:
- `llama-3.1-8b-instant` (default, fast & accurate)
- `mixtral-8x7b-32768` (more powerful)
- `gemma-7b-it` (lightweight)

### Temperature
- **0.0** → Deterministic, reliable (recommended for code)
- **0.5–0.7** → Balanced
- **1.0+** → Creative but risky

### Max Iterations
- **3–5** → Good for simple tasks
- **5–10** → For harder debugging scenarios

---

## What Can It Do?

### ✅ Excels At
- Algorithms (sorting, searching, math)
- Data processing and transformations
- API calls and web requests
- File I/O operations
- String manipulation
- Basic scraping
- Logic-heavy single-file scripts

### ⚠️ Limitations
- Not for multi-file projects (yet)
- Requires installed dependencies in runtime environment
- Bounded by LLM knowledge cutoff
- Can't install packages dynamically
- Best for scripts under ~500 lines

---

## Agentic AI Concepts

This project demonstrates:

**Reflexion** — The agent observes its own output and uses that feedback to improve.

**Closed-Loop System** — Instead of one-shot generation, there's a feedback mechanism:
```
Generate → Execute → Observe Error → Refine → Repeat
```

**Autonomous Iteration** — The agent decides to retry without human intervention.

**Tool Use** — The subprocess execution is a "tool" the agent uses to validate its own work.

---

## Tech Stack

- **Streamlit** — Web UI and state management
- **Groq API** — LLM inference (via official SDK)
- **Python subprocess** — Code execution
- **Regex** — Code block extraction
- **dotenv** — Environment variable management

---

## Environment Variables

Create a `.env` file in the root directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free Groq API key: [console.groq.com](https://console.groq.com)

---

## Performance

Typical execution times (on Groq):
- Simple task (1 iteration): ~2–3 seconds
- Task with 1 retry: ~4–6 seconds
- Complex task (3–5 iterations): ~10–20 seconds

Times vary based on task complexity, network latency, and Groq API load.

---

## Why This Matters

This project shows:
- **System thinking**: Combining multiple components (UI, LLM, execution, error handling)
- **Agentic AI understanding**: How agents observe their environment and adapt
- **Practical GenAI**: Moving beyond static generation to interactive, validating systems
- **Engineering maturity**: Clear scope, honest limitations, safe design

---

## Common Questions

### Q: Is this a replacement for a full IDE?
**A:** No. It's best for quick prototyping, validation, and learning. For production code and large projects, use a proper IDE.

### Q: Can it generate code in other languages?
**A:** Currently Python-only. Extending to JavaScript, Go, etc. would require runtime environments for each language.

### Q: What if the AI can't fix the code?
**A:** After max iterations, you see the last attempt and full debug history. You can manually refine or try a simpler task.

### Q: Is my code data private?
**A:** Code is sent to Groq's API. Use your own API key. Don't submit sensitive production code.

### Q: Can I use other LLMs?
**A:** Yes—modify the `_ask_model()` method in `reflexion_agent.py` to use OpenAI, Anthropic, or other providers.

---

## Roadmap

- [ ] Support for multiple languages (JavaScript, Go, Rust)
- [ ] Web app context (HTML/CSS generation)
- [ ] Package auto-installation
- [ ] Session persistence (save/load previous runs)
- [ ] Parallel iteration testing
- [ ] Custom system prompts per task type

---

## Contributing

Contributions welcome! Areas of interest:
- New language support
- Better error recovery strategies
- UI/UX improvements
- Performance optimization
- Test suite expansion

Feel free to open issues and PRs.

## Author

Built with curiosity about agentic AI and the power of execution feedback loops.

**Feedback & Questions?** Open an issue or reach out on GitHub.

---

## One-Sentence Summary

> This project demonstrates how an AI agent can iteratively generate and validate Python code using execution feedback, rather than just producing static answers.

---


