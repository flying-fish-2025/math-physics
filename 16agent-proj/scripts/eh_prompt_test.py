from __future__ import annotations

import json
import os

from math_agent_mcp.mcp_tool_executor import MCPToolExecutor


def main() -> None:
    os.environ.setdefault("OPENAI_BASE_URL", "https://hiapi.online/v1")
    os.environ.setdefault("MODEL_PRIMARY", "gemini-3-flash-no")
    os.environ.setdefault("MODEL_FALLBACK", "gemini-3-pro-no")
    q = "用mcp或skill工具从Einstein Hilbert作用量推到Einstein场方程，并给出latex形式化中间过程。"
    ex = MCPToolExecutor(kb_dir="kb", max_steps=8)
    out = ex.run(q, auto_upgrade=True)
    brief = {
        "model": out.get("model"),
        "trace_count": len(out.get("traces", [])),
        "tools": [t.get("tool") for t in out.get("traces", [])],
        "proof_head": (out.get("proof", "")[:500]),
    }
    print(json.dumps(brief, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

