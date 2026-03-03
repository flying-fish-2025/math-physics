from __future__ import annotations

import json

from math_agent_mcp.tools.knowledge_tools import search_knowledge


def main() -> None:
    hits = search_knowledge("当前用户是谁 陈可为", kb_dir="kb", top_k=3)
    print(json.dumps(hits, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

