from __future__ import annotations

import json

from math_agent_mcp.tools.cadabra_tools import run_cadabra
from math_agent_mcp.tools.mathematica_tools import run_mathematica


def main() -> None:
    result = {
        "cadabra": run_cadabra("x:=x;"),
        "mathematica": run_mathematica("2+2"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

