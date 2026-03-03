from __future__ import annotations

import json

from math_agent_mcp.mcp_tool_executor import MCPToolExecutor


def main() -> None:
    executor = MCPToolExecutor(kb_dir="kb", max_steps=8)
    out = executor.run("求解微分方程 dy/dx=sin(x)，并进行回代验证。")
    verify = out.get("verify_result")
    rerun = executor.verify_last(out)
    payload = {
        "model": out.get("model"),
        "upgraded": out.get("upgraded"),
        "auto_verify": verify,
        "manual_verify": rerun,
        "trace_count": len(out.get("traces", [])),
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

