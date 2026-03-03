from __future__ import annotations

import os
import platform
import shlex
import subprocess
from typing import Any


def _run(cmd: list[str], script: str) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            cmd,
            input=script,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return {
            "ok": False,
            "error": "command not found",
            "command": cmd,
        }

    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "returncode": proc.returncode,
        "command": cmd,
    }


def run_cadabra(script: str) -> dict[str, Any]:
    """
    Hybrid strategy:
    1) try local CADABRA2_BIN/cadabra2
    2) on Windows, fallback to WSL micromamba env (default: cadabra)
    """
    cadabra_bin = os.getenv("CADABRA2_BIN", "cadabra2")
    local = _run([cadabra_bin], script)
    if local.get("ok"):
        local["backend"] = "local"
        return local
    if local.get("error") != "command not found":
        local["backend"] = "local"
        return local

    if platform.system().lower().startswith("win"):
        wsl_env = os.getenv("CADABRA2_WSL_ENV", "cadabra")
        wsl_launcher = os.getenv("CADABRA2_WSL_LAUNCHER", "micromamba")
        wsl_cmd = f"{shlex.quote(wsl_launcher)} run -n {shlex.quote(wsl_env)} cadabra2"
        wsl = _run(["wsl", "bash", "-lc", wsl_cmd], script)
        if wsl.get("ok"):
            wsl["backend"] = "wsl"
            return wsl
        wsl["backend"] = "wsl"
        return {
            "ok": False,
            "error": (
                "cadabra2 not found locally and WSL fallback failed. "
                "Set CADABRA2_BIN or ensure `wsl bash -lc \"micromamba run -n cadabra cadabra2 -\"` works."
            ),
            "local_attempt": local,
            "wsl_attempt": wsl,
        }

    return {
        "ok": False,
        "error": "cadabra2 not found. Set CADABRA2_BIN or install Cadabra2.",
        "local_attempt": local,
    }
