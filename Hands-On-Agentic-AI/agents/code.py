from pathlib import Path
import subprocess

SANDBOX_DIR = Path("./sandbox").resolve()

def write_file(filename, content):
    path = (SANDBOX_DIR / filename).resolve()

    if SANDBOX_DIR not in path.parents:
        raise ValueError("Refusing to write outside sandbox")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    return str(path.relative_to(SANDBOX_DIR))


def read_file(filename, max_bytes=10000):
    path = (SANDBOX_DIR / filename).resolve()

    if SANDBOX_DIR not in path.parents and path != SANDBOX_DIR:
        raise ValueError("Refusing to read outside sandbox")

    if not path.exists():
        raise FileNotFoundError(f"{filename} does not exist")

    if path.is_dir():
        raise IsADirectoryError(f"{filename} is a directory")

    raw = path.read_bytes()
    total_len = len(raw)

    truncated = raw[:max_bytes]
    text = truncated.decode("utf-8", errors="replace")

    if total_len > max_bytes:
        text += f"\n... (output truncated, length: {total_len})"

    return text


def run_command(command, timeout=60):
    result = subprocess.run(
        command,
        cwd=SANDBOX_DIR,
        shell=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )

    return {
        "command": command,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }
