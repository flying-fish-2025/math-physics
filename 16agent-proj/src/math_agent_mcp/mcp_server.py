from __future__ import annotations

import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from math_agent_mcp.session_manager import SessionManager
from math_agent_mcp.tools.cadabra_tools import run_cadabra
from math_agent_mcp.tools.knowledge_tools import search_knowledge
from math_agent_mcp.tools.mathematica_tools import run_mathematica
from math_agent_mcp.tools.sympy_tools import canonicalise, solve_ode, verify_substitution


mcp = FastMCP("math-physics-proof-mcp")
sessions = SessionManager()


def _ensure_session(session_id: str | None) -> str:
    state = sessions.get_or_create(session_id)
    return state.session_id


@mcp.tool()
def create_session() -> dict[str, Any]:
    state = sessions.create_session()
    return {"session_id": state.session_id, "created_at": state.created_at}


@mcp.tool()
def list_session_objects(session_id: str) -> dict[str, Any]:
    return {"session_id": session_id, "objects": sessions.list_objects(session_id)}


@mcp.tool()
def get_session_traces(session_id: str) -> dict[str, Any]:
    return {"session_id": session_id, "traces": sessions.get_traces(session_id)}


@mcp.tool()
def define_expression(name: str, expr_str: str, session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    sessions.put_object(sid, name, expr_str)
    result = {"session_id": sid, "name": name, "expr_str": expr_str}
    sessions.trace(sid, "define_expression", {"name": name, "expr_str": expr_str}, result)
    return result


@mcp.tool()
def sympy_canonicalise(expr_str: str, session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    reduced = canonicalise(expr_str)
    result = {"session_id": sid, "input": expr_str, "output": reduced}
    sessions.trace(sid, "sympy_canonicalise", {"expr_str": expr_str}, result)
    return result


@mcp.tool()
def sympy_canonicalise_object(name: str, session_id: str) -> dict[str, Any]:
    expr = sessions.get_object(session_id, name)
    reduced = canonicalise(str(expr))
    sessions.put_object(session_id, name, reduced)
    result = {"session_id": session_id, "name": name, "output": reduced}
    sessions.trace(session_id, "sympy_canonicalise_object", {"name": name}, result)
    return result


@mcp.tool()
def sympy_dsolve_ode(eq_str: str, y_name: str = "y", x_name: str = "x", session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    solution = solve_ode(eq_str=eq_str, y_name=y_name, x_name=x_name)
    result = {"session_id": sid, "equation": eq_str, "solution": solution}
    sessions.trace(
        sid,
        "sympy_dsolve_ode",
        {"eq_str": eq_str, "y_name": y_name, "x_name": x_name},
        result,
    )
    return result


@mcp.tool()
def sympy_verify_substitution(
    eq_str: str,
    solution_str: str,
    y_name: str = "y",
    x_name: str = "x",
    session_id: str | None = None,
) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    verify = verify_substitution(eq_str, solution_str, y_name=y_name, x_name=x_name)
    result = {"session_id": sid, "equation": eq_str, "solution": solution_str, "verify": verify}
    sessions.trace(
        sid,
        "sympy_verify_substitution",
        {"eq_str": eq_str, "solution_str": solution_str, "y_name": y_name, "x_name": x_name},
        result,
    )
    return result


@mcp.tool()
def cadabra_run(script: str, session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    out = run_cadabra(script)
    result = {"session_id": sid, "result": out}
    sessions.trace(sid, "cadabra_run", {"script": script}, out)
    return result


@mcp.tool()
def mathematica_run(code: str, session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    out = run_mathematica(code)
    result = {"session_id": sid, "result": out}
    sessions.trace(sid, "mathematica_run", {"code": code}, out)
    return result


@mcp.tool()
def knowledge_search(query: str, kb_dir: str = "kb", top_k: int = 3, session_id: str | None = None) -> dict[str, Any]:
    sid = _ensure_session(session_id)
    hits = search_knowledge(query=query, kb_dir=kb_dir, top_k=top_k)
    result = {"session_id": sid, "query": query, "hits": hits}
    sessions.trace(
        sid,
        "knowledge_search",
        {"query": query, "kb_dir": kb_dir, "top_k": top_k},
        {"count": len(hits)},
    )
    return result


@mcp.tool()
def export_session_json(session_id: str) -> str:
    payload = sessions.export_session(session_id)
    return json.dumps(payload, ensure_ascii=False, indent=2)


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

