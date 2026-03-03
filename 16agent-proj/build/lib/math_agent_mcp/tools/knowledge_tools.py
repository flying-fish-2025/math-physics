from __future__ import annotations

from pathlib import Path
import re


def _tokenize(text: str) -> list[str]:
    base = [t.lower() for t in re.findall(r"[A-Za-z0-9_\-\u4e00-\u9fff]+", text)]
    enriched: list[str] = []
    for tok in base:
        enriched.append(tok)
        # Add single-character Chinese tokens for better Chinese retrieval overlap.
        if re.search(r"[\u4e00-\u9fff]", tok):
            enriched.extend([c for c in tok if re.match(r"[\u4e00-\u9fff]", c)])
    return enriched


def _build_preview(text: str, query: str) -> str:
    q_tokens = _tokenize(query)
    for tok in q_tokens:
        if len(tok) < 2:
            continue
        idx = text.lower().find(tok.lower())
        if idx >= 0:
            start = max(0, idx - 80)
            end = min(len(text), idx + 220)
            return text[start:end].replace("\n", " ")
    return text[:300].replace("\n", " ")


def search_knowledge(query: str, kb_dir: str = "kb", top_k: int = 3) -> list[dict]:
    root = Path(kb_dir)
    if not root.exists():
        return []

    q_tokens = set(_tokenize(query))
    hits: list[dict] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".txt"}:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        tokens = set(_tokenize(text))
        overlap = len(q_tokens.intersection(tokens))
        if overlap == 0:
            continue
        hits.append(
            {
                "path": str(p),
                "score": overlap,
                "preview": _build_preview(text, query),
            }
        )

    hits.sort(key=lambda x: x["score"], reverse=True)
    return hits[:top_k]

