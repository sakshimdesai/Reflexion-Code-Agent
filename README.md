# Reflexion Code Agent

> **Generate. Execute. Reflect. Repair.**

A self-correcting Python code generation agent that doesn't stop at writing code.

**Reflexion Code Agent** takes a natural-language programming task, asks an LLM to generate a Python program, executes that program locally, observes the real runtime result, and — when execution fails — sends the failure back to the model so it can generate a corrected version.

The key idea is simple:

```text
LLM output → Real execution → Runtime feedback → LLM correction → Re-execution

Instead of treating code generation as a one-shot interaction, this project turns it into a closed feedback loop.

Why this project?

Most AI coding workflows look like this:

Ask AI
   ↓
Copy code
   ↓
Run code
   ↓
Get an error
   ↓
Copy error back to AI
   ↓
Try again

This project automates that loop.

             ┌──────────────────────┐
             │   Natural-language   │
             │        task          │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │    LLM generates     │
             │     Python code      │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │   Execute generated  │
             │        code          │
             └──────────┬───────────┘
                        ↓
                 ┌──────┴──────┐
                 │             │
              Success        Failure
                 │             │
                 ↓             ↓
              Finish     Capture stderr
                               │
                               ↓
                         Feed back to LLM
                               │
                               ↓
                         Generate repair
                               │
                               └──────→ Execute again

The important distinction is that the agent receives feedback from an actual execution environment, not just another conversational response.

What it does
1. Generate

Describe a Python programming task in natural language.

Example:

Calculate the 1000th Fibonacci number using recursion with memoization and verify that the result contains more than 200 digits.

The LLM generates a complete Python script.

2. Execute

The generated script is written to the agent's workspace and executed using Python's subprocess module.

The agent captures:

stdout
stderr
process exit code

This means the generated code is actually run rather than merely displayed.

3. Observe

If execution fails, the agent records the runtime failure.

For example:

ExitCode != 0
STDERR:
RecursionError: maximum recursion depth exceeded
4. Reflect

The runtime error is sent back to the LLM as feedback.

The model receives the failure and is asked to produce a corrected version.

5. Repair

The corrected program is executed again.

The cycle continues until:

execution succeeds, or
the configured maximum number of iterations is reached.
A real Reflexion run

One of the project's demo tasks asks the agent to calculate Fibonacci(1000) using recursive memoization.

The first generated implementation encountered a real runtime failure.

The Reflexion trace showed:

Code generated
Execution failed — feedback returned to agent
Code generated
Execution passed

The run completed in 2 iterations.

The repaired version successfully produced Fibonacci(1000):

434665576869374564356885276750406258025646605173717804024817...

The result contains 209 digits, satisfying the task's requirement that it contain more than 200 digits.

The execution details showed:

Iteration 2 — ExitCode=0

STDERR:

The significance of this example is not the Fibonacci calculation itself.

It demonstrates the complete loop:

Generate
   ↓
Execute
   ↓
Observe real failure
   ↓
Return failure to agent
   ↓
Generate correction
   ↓
Execute successfully
Another example

The agent can also solve straightforward programming tasks in a single iteration.

Example task:

Generate 100 random integers between 1 and 1000, find the 10 largest prime numbers, and print them in descending order.

Example result:

10 largest primes (descending):
[991, 839, 797, 733, 617, 593, 521, 467, 461, 379]

Here the generated program completed successfully on the first execution.

This gives two useful modes of behavior:

Simple task
    ↓
Generate → Execute → Success


Task requiring correction
    ↓
Generate → Execute → Failure
                   ↓
                Feedback
                   ↓
                Repair
                   ↓
                Execute → Success
Architecture

The project is intentionally small: the core agent is separated from the Streamlit interface.

                         ┌───────────────────┐
                         │       User        │
                         │  Natural language │
                         │       task        │
                         └─────────┬─────────┘
                                   │
                                   ▼
                         ┌───────────────────┐
                         │    Streamlit UI   │
                         │      app.py       │
                         └─────────┬─────────┘
                                   │
                                   ▼
                    ┌────────────────────────────┐
                    │   ReflexionCodeAgent       │
                    │  reflexion_agent.py        │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    Groq LLM     │
                         │ Code generation │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Code extraction │
                         │  & file write   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Python process  │
                         │   subprocess    │
                         └────────┬────────┘
                                  │
                         ┌────────┴────────┐
                         ▼                 ▼
                      stdout            stderr
                         │                 │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Exit code /     │
                         │ runtime result  │
                         └────────┬────────┘
                                  │
                           failure detected
                                  │
                                  ▼
                         ┌─────────────────┐
                         │ Feedback to LLM │
                         └────────┬────────┘
                                  │
                                  └──────→ next iteration
Core implementation

The agent's main loop is intentionally straightforward:

for iteration in range(1, max_iterations + 1):

    generated_code = ask_model(...)

    save_code(generated_code)

    exit_code, stdout, stderr = run_code(...)

    if exit_code == 0:
        return success

    send_error_back_to_model(stderr)

The important engineering boundary is between generation and execution.

The LLM proposes the solution.

The runtime provides evidence about whether that solution actually executes successfully.

Project structure
Reflexion-Code-Agent/
│
├── app.py
│   └── Streamlit interface
│
├── reflexion_agent.py
│   └── Core generation, execution, feedback and retry loop
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
│   └── Environment secrets and generated runtime files
│
└── code_workspace/
    └── Runtime-generated files and execution logs

code_workspace/ is runtime-generated and is intentionally excluded from version control.

app.py

The Streamlit frontend is responsible for the user-facing experience.

It handles:

task input
generation and execution controls
displaying generated Python
displaying execution output
execution details
Reflexion trace
debugging history
Python file export

The current interface is intentionally minimal and focused around the core loop:

GENERATE · EXECUTE · REFLECT · REPAIR
reflexion_agent.py

This file contains the core agent logic.

The agent:

Sends the task to the LLM.
Extracts Python code from the response.
Writes the generated program to the workspace.
Executes it using the same Python interpreter running the application.
Captures stdout, stderr, and the exit code.
Records execution logs.
Feeds runtime errors back to the model when execution fails.
Repeats until success or the iteration limit is reached.

The current implementation uses a default maximum of 5 iterations.

Tech Stack
Component	Technology
Language	Python
UI	Streamlit
LLM API	Groq
Default model	openai/gpt-oss-20b
Alternative model	openai/gpt-oss-120b
Code execution	Python subprocess
Environment variables	python-dotenv
Code extraction	Python regular expressions
Runtime logging	File-based stdout/stderr logs
Getting Started
Prerequisites
Python 3.8+
A Groq API key
1. Clone the repository
git clone https://github.com/sakshimdesai/Reflexion-Code-Agent.git
cd Reflexion-Code-Agent
2. Create a virtual environment
Windows
python -m venv venv
venv\Scripts\activate
macOS / Linux
python -m venv venv
source venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure your API key

Create a local .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

Never commit .env or a real API key to Git.

The repository's .gitignore excludes .env.

5. Run the application
streamlit run app.py

Then open the local Streamlit URL shown in the terminal, typically:

http://localhost:8501
What makes it an agent?

A code generator can produce a program.

An agent needs to interact with an environment and use the result of that interaction to decide what to do next.

This project demonstrates that pattern:

                    ┌──────────────┐
                    │     LLM      │
                    └──────┬───────┘
                           │
                      Generate code
                           │
                           ▼
                    ┌──────────────┐
                    │   Runtime    │
                    └──────┬───────┘
                           │
                     Observe result
                           │
                    ┌──────┴───────┐
                    │              │
                  Success        Failure
                    │              │
                    ▼              ▼
                  Finish       Feedback
                                   │
                                   ▼
                              LLM revises
                                   │
                                   └──→ Runtime

The runtime therefore becomes part of the agent's feedback loop.

The model isn't simply asked:

"Is this code correct?"

It gets evidence from actually executing the generated program.

Design Decisions
Real execution instead of simulated validation

Generated code is executed through Python's subprocess module.

This gives the agent access to actual runtime behavior such as:

exceptions
exit codes
standard output
standard error
Error-driven iteration

A failed execution is not treated as the end of the task.

The captured error becomes input to the next generation step.

Bounded retries

The agent does not retry indefinitely.

A maximum iteration count bounds the loop and prevents an unsuccessful task from running forever.

Separate UI and agent logic

The Streamlit application handles presentation and interaction, while reflexion_agent.py contains the core generation/execution loop.

This keeps the agent logic independent from the interface.

Current Scope

The project is designed primarily around single-file Python programs.

It is well suited to tasks such as:

algorithms
mathematical programs
data transformations
file-processing scripts
API-oriented Python scripts
string and logic manipulation
small standalone programs

It is not intended to replace a full IDE or serve as a complete autonomous software-development environment.

Generated programs also execute in the local runtime environment, so their behavior depends on the available Python version, installed dependencies, filesystem, and other runtime conditions.

Known Limitations

The current implementation has several deliberate boundaries:

Python-only code generation and execution
Primarily designed for standalone/single-file programs
No automatic package installation
Limited to the configured number of iterations
Successful process exit does not by itself guarantee semantic correctness
Generated code executes locally, so arbitrary generated programs should be treated carefully
The agent depends on the capabilities and behavior of the selected LLM

These limitations are part of the current scope rather than hidden assumptions.

Security Note

The application executes LLM-generated Python code locally.

That means generated code should be treated as untrusted code.

Do not use the agent with sensitive files, credentials, production environments, or other resources you do not want generated code to access.

API credentials are loaded from environment variables and should never be committed to the repository.

Future Directions

Possible extensions include:

stronger task-level output verification
safer isolated execution environments
richer execution policies
multi-file project support
additional programming languages
persistent sessions
more structured agent feedback
automated test generation and validation

These are directions for future development, not currently implemented features.

The Core Idea

The interesting part of this project isn't that an LLM can write Python.

LLMs can already do that.

The interesting part is what happens after the code is generated.

Generate
   ↓
Execute
   ↓
Observe
   ↓
Reflect
   ↓
Repair
   ↓
Execute again

That small feedback loop changes the interaction from:

"Give me some code."

to:

"Try to solve this, see what actually happens, and improve the solution when reality disagrees with you."

Author

Sakshi M Desai

Built as an exploration of:

agentic AI
execution feedback loops
LLM-powered programming
runtime-driven self-correction
practical AI engineering
One-line summary

Reflexion Code Agent is a Python coding agent that generates programs, executes them for real, observes runtime failures, and uses those failures as feedback to iteratively repair its own output.
