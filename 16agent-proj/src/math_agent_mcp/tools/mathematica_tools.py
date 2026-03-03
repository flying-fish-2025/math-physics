from __future__ import annotations

import os
from pathlib import Path
import subprocess


def _candidate_bins() -> list[str]:
    configured = os.getenv("MATHEMATICA_BIN", "").strip()
    candidates: list[str] = []
    if configured:
        candidates.append(configured)

    candidates.append("wolframscript")

    program_files = os.getenv("ProgramFiles", r"C:\Program Files")
    wolfram_root = Path(program_files) / "Wolfram Research"
    if wolfram_root.exists():
        for p in wolfram_root.rglob("wolframscript.exe"):
            candidates.append(str(p))
    return candidates


def run_mathematica(code: str) -> dict:
    last_error = "wolframscript not found"
    proc = None
    cmd = []
    for wolfram_bin in _candidate_bins():
        cmd = [wolfram_bin, "-code", code]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            break
        except FileNotFoundError:
            continue
        except OSError as exc:
            last_error = str(exc)
            continue

    if proc is None:
        return {"ok": False, "error": f"{last_error}. Set MATHEMATICA_BIN if needed."}

    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
        "command": cmd,
    }

