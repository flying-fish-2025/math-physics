from __future__ import annotations

import json

from math_agent_mcp.llm_client import smoke_test_chat


def main() -> None:
    result = smoke_test_chat()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

