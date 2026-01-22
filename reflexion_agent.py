import os
import re
import subprocess
import sys
import time
import datetime
import pathlib
from dotenv import load_dotenv

# try to import Groq SDK
try:
    from groq import Groq
except Exception:
    Groq = None

load_dotenv()
GROQ_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_KEY:
    print("⚠️  Warning: GROQ_API_KEY not found in .env file")

if Groq and GROQ_KEY:
    client = Groq(api_key=GROQ_KEY)
else:
    client = None

# regex to extract python code blocks
CODE_BLOCK_RE = re.compile(r"```(?:python)?\n(.*?)```", re.S)


class ReflexionCodeAgent:
    """
    A self-correcting code generation agent:
    - Generates Python code from natural language
    - Executes it locally using subprocess
    - Captures output/errors
    - Fixes code automatically until success
    """

    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        max_iterations: int = 5,
        timeout: int = 60,
        temperature: float = 0.0,
        workspace: str = "code_workspace",
    ):
        self.model = model
        self.max_iterations = max_iterations
        self.timeout = timeout
        self.temperature = temperature
        self.workspace = workspace
        os.makedirs(self.workspace, exist_ok=True)

    # -------------------------------
    # Low-level Groq model call
    # -------------------------------
    def _ask_model(self, messages):
        if client is None:
            raise RuntimeError("Groq client not available or GROQ_API_KEY not set.")

        resp = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1500,
        )

        try:
            return resp.choices[0].message["content"]
        except Exception:
            try:
                return resp.choices[0].message.content
            except Exception:
                try:
                    return resp.choices[0].text
                except Exception:
                    return str(resp)

    # -------------------------------
    # Extract Python code block
    # -------------------------------
    def _extract_code(self, text: str) -> str:
        if not isinstance(text, str):
            return ""
        m = CODE_BLOCK_RE.search(text)
        if m:
            return m.group(1).strip()
        # fallback heuristic
        if text.strip().startswith(("def ", "import ", "from ", "#!/usr/bin/env python")):
            return text.strip()
        return ""

    # -------------------------------
    # Run generated code for real
    # -------------------------------
    def _run_code(self, filename):
        """
        Run the generated python file using the same Python interpreter (venv).
        Capture stdout/stderr to code_workspace/run_logs/ and return (exitcode, out, err).
        """
        logs_dir = pathlib.Path(self.workspace) / "run_logs"
        logs_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_stem = logs_dir / f"run_{ts}"

        python_exec = sys.executable  # use same python as Streamlit (venv)
        cmd = [python_exec, filename]

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=max(self.timeout, 120)
            )
            out, err = proc.stdout, proc.stderr
            # write logs for debugging
            (log_stem.with_suffix(".out.txt")).write_text(out or "", encoding="utf-8")
            (log_stem.with_suffix(".err.txt")).write_text(err or "", encoding="utf-8")
            (log_stem.with_suffix(".cmd.txt")).write_text(" ".join(cmd), encoding="utf-8")
            return proc.returncode, out, err
        except subprocess.TimeoutExpired:
            (log_stem.with_suffix(".err.txt")).write_text("TimeoutExpired", encoding="utf-8")
            return -1, "", "TimeoutExpired"
        except Exception as e:
            (log_stem.with_suffix(".err.txt")).write_text(str(e), encoding="utf-8")
            return -1, "", str(e)

    # -------------------------------
    # Main Reflexion loop
    # -------------------------------
    def generate_code(self, task_prompt: str):
        """
        Generate, run, and iteratively fix code for a given task.
        Returns dict: { success, code, iterations, history }
        """
        system_msg = (
            "You are an expert Python programmer. "
            "Always respond with a fenced Python code block ```python\\n...``` that can run standalone."
        )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": f"Task: {task_prompt}\nWrite a complete Python script that performs this task."},
        ]

        history = []
        for i in range(1, self.max_iterations + 1):
            assistant_text = self._ask_model(messages)
            history.append({"role": "assistant", "content": assistant_text})

            code = self._extract_code(assistant_text)
            if not code:
                return {"success": False, "code": "", "iterations": i, "history": history}

            # Save generated code
            temp_path = os.path.join(self.workspace, "task.py")
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(code + "\n")

            # Run it
            exitcode, out, err = self._run_code(temp_path)
            history.append({"role": "executor", "content": f"Iteration {i} — ExitCode={exitcode}\nSTDOUT:\n{out}\nSTDERR:\n{err}"})

            # Success
            if exitcode == 0:
                return {"success": True, "code": code, "iterations": i, "history": history}

            # Feed back the error to the model
            messages.append({"role": "assistant", "content": assistant_text})
            messages.append({
                "role": "user",
                "content": f"The script failed with ExitCode={exitcode}. STDERR:\n{err}\nPlease fix the error and provide a corrected script."
            })

            time.sleep(0.5)

        # Max iterations reached — failed
        final_code = ""
        try:
            final_code = open(os.path.join(self.workspace, "task.py"), "r", encoding="utf-8").read()
        except Exception:
            final_code = ""

        return {"success": False, "code": final_code, "iterations": self.max_iterations, "history": history}

    # -------------------------------
    # Aliases for compatibility
    # -------------------------------
    def generate_and_fix(self, task_prompt: str):
        return self.generate_code(task_prompt)

    def generate(self, task_prompt: str):
        return self.generate_code(task_prompt)


# ------------------------------------------------------
# Test the agent directly (optional)
# ------------------------------------------------------
if __name__ == "__main__":
    agent = ReflexionCodeAgent()
    print("🧪 Testing Reflexion Agent...")
    result = agent.generate_code("Print the first 10 Fibonacci numbers")
    print("✅ Success:", result["success"])
    print("🔄 Iterations:", result["iterations"])
    print("📝 Code:\n", result["code"])