from __future__ import annotations

import sympy as sp


def parse_expr(expr_str: str):
    return sp.sympify(expr_str)


def _normalize_equation_str(eq_str: str) -> str:
    raw = eq_str.strip()
    if raw.startswith("Eq("):
        return raw
    if "=" in raw:
        lhs, rhs = raw.split("=", 1)
        return f"Eq({lhs.strip()}, {rhs.strip()})"
    return raw


def canonicalise(expr_str: str) -> str:
    expr = parse_expr(expr_str)
    return str(sp.simplify(expr))


def solve_ode(eq_str: str, y_name: str = "y", x_name: str = "x") -> str:
    x = sp.Symbol(x_name)
    y = sp.Function(y_name)
    eq = parse_expr(_normalize_equation_str(eq_str))
    sol = sp.dsolve(eq, y(x))
    return str(sol)


def verify_substitution(eq_str: str, solution_str: str, y_name: str = "y", x_name: str = "x") -> dict:
    x = sp.Symbol(x_name)
    y = sp.Function(y_name)
    eq = parse_expr(_normalize_equation_str(eq_str))
    solution = parse_expr(solution_str)

    if not isinstance(solution, sp.Equality):
        return {"ok": False, "reason": "solution must be an Equality like Eq(y(x), ...)"}

    rhs = solution.rhs
    substituted = eq.subs(y(x), rhs).doit()
    reduced = sp.simplify(substituted.lhs - substituted.rhs) if isinstance(substituted, sp.Equality) else sp.simplify(substituted)
    is_valid = reduced == 0 or reduced is True or reduced == sp.S.true
    residual = "0" if is_valid else str(reduced)
    return {"ok": bool(is_valid), "residual": residual}

