from __future__ import annotations

import json

from math_agent_mcp.mcp_tool_executor import MCPToolExecutor


def main() -> None:
    executor = MCPToolExecutor(kb_dir="kb", max_steps=4)
    out = executor.run("化简表达式 sin(x)^2+cos(x)^2")
    payload = {
        "model": out.get("model"),
        "upgraded": out.get("upgraded"),
        "verify_result": out.get("verify_result"),
        "proof_preview": (out.get("proof") or "")[:240],
        "trace_count": len(out.get("traces", [])),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

