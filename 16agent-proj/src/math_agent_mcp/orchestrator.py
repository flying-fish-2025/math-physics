from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from math_agent_mcp.tools.knowledge_tools import search_knowledge
from math_agent_mcp.tools.sympy_tools import canonicalise, solve_ode, verify_substitution


@dataclass
class StepTrace:
    tool: str
    args: dict[str, Any]
    result: Any


class DerivationOrchestrator:
    """
    Lightweight orchestrator for demo UI.
    In production you can replace this with GPT/Gemini MCP tool-calling loop.
    """

    def __init__(self, kb_dir: str = "kb") -> None:
        self.kb_dir = kb_dir

    @staticmethod
    def _looks_like_simple_ode(problem: str) -> bool:
        p = problem.lower().replace(" ", "")
        return "dy/dx=" in p or "eq(derivative(y(x),x)," in p

    @staticmethod
    def _normalize_ode(problem: str) -> str:
        p = problem.strip().replace(" ", "")
        m = re.search(r"dy/dx=(.+)", p, flags=re.IGNORECASE)
        if m:
            rhs = m.group(1)
            return f"Eq(Derivative(y(x), x), {rhs})"
        return problem

    def run(self, problem: str, model_hint: str = "gemini3") -> dict[str, Any]:
        traces: list[StepTrace] = []

        kb_hits = search_knowledge(problem, kb_dir=self.kb_dir, top_k=3)
        traces.append(
            StepTrace(
                tool="knowledge_search",
                args={"query": problem, "kb_dir": self.kb_dir, "top_k": 3},
                result=kb_hits,
            )
        )

        if self._looks_like_simple_ode(problem):
            eq_str = self._normalize_ode(problem)
            traces.append(
                StepTrace(
                    tool="sympy_normalize_ode",
                    args={"problem": problem},
                    result=eq_str,
                )
            )
            sol = solve_ode(eq_str, y_name="y", x_name="x")
            traces.append(
                StepTrace(
                    tool="sympy_dsolve_ode",
                    args={"eq_str": eq_str, "y_name": "y", "x_name": "x"},
                    result=sol,
                )
            )
            verify = verify_substitution(eq_str, sol, y_name="y", x_name="x")
            traces.append(
                StepTrace(
                    tool="sympy_verify_substitution",
                    args={"eq_str": eq_str, "solution_str": sol},
                    result=verify,
                )
            )

            proof = (
                f"模型偏好: {model_hint}\n\n"
                "证明过程（工具驱动）:\n"
                f"1) 将输入标准化为方程: {eq_str}\n"
                f"2) 使用 SymPy dsolve 得到通解: {sol}\n"
                f"3) 代回原方程验证: {verify}\n\n"
                "结论: 该结果由工具返回并通过代回验算，非 LLM 心算得到。"
            )
            return {"proof": proof, "traces": [t.__dict__ for t in traces]}

        reduced = canonicalise(problem)
        traces.append(
            StepTrace(
                tool="sympy_canonicalise",
                args={"expr_str": problem},
                result=reduced,
            )
        )
        proof = (
            f"模型偏好: {model_hint}\n\n"
            "这是一个表达式化简任务:\n"
            f"- 原表达式: {problem}\n"
            f"- SymPy 化简结果: {reduced}\n\n"
            "结论: 结果由工具计算返回。"
        )
        return {"proof": proof, "traces": [t.__dict__ for t in traces]}

