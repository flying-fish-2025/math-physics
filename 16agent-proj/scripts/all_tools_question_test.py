from __future__ import annotations

import json

from math_agent_mcp.mcp_server import (
    cadabra_run,
    knowledge_search,
    mathematica_run,
    sympy_canonicalise,
    sympy_dsolve_ode,
    sympy_verify_substitution,
)


def main() -> None:
    question = "请验证三角恒等式并求解 dy/dx=sin(x)"

    result = {
        "question": question,
        "knowledge_search": knowledge_search(query=question, kb_dir="kb", top_k=3),
        "sympy_canonicalise": sympy_canonicalise("sin(x)**2 + cos(x)**2"),
        "sympy_dsolve_ode": sympy_dsolve_ode("Eq(Derivative(y(x), x), sin(x))"),
        "cadabra_run": cadabra_run("x:=x;"),
        "mathematica_run": mathematica_run("2+2"),
    }

    ode = result["sympy_dsolve_ode"]
    result["sympy_verify_substitution"] = sympy_verify_substitution(
        eq_str=ode["equation"],
        solution_str=ode["solution"],
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

