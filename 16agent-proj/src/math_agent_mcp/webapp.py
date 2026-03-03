from __future__ import annotations

import json
import os

import streamlit as st

from math_agent_mcp.mcp_tool_executor import MCPToolExecutor

TEST_QUESTIONS = [
    "求解微分方程 dy/dx=sin(x)，并进行回代验证。",
    "化简表达式 sin(x)^2 + cos(x)^2，并说明依据。",
    "用 SymPy 求解方程 x^2 - 5*x + 6 = 0，并检查解是否正确。",
    "计算并化简 (x+y)^4 的展开式。",
    "给出一个 Cadabra2 示例：定义 x:=x 并返回结果。",
    "用 Mathematica 计算 Integrate[Sin[x], x]，并与 SymPy 结果对比。",
    "检索知识库：一阶常微分方程的通用求解思路。",
    "验证 y(x)=C1-cos(x) 是否满足 Derivative(y(x), x)=sin(x)。",
]


st.set_page_config(page_title="数学/物理证明 Agent", page_icon="∫", layout="wide")
st.title("数学/物理证明 Agent（MCP 工具链）")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_run" not in st.session_state:
    st.session_state.last_run = None


def _build_export_text(history: list[dict]) -> str:
    lines: list[str] = []
    for i, item in enumerate(history, start=1):
        role = item.get("role", "unknown")
        lines.append(f"[{i}] {role.upper()}")
        lines.append(item.get("content", ""))
        if role == "assistant" and isinstance(item.get("run"), dict):
            run = item["run"]
            lines.append(f"model={run.get('model')}")
            if run.get("upgraded"):
                lines.append(
                    f"upgraded: {run.get('primary_model')} -> {run.get('fallback_model')} "
                    f"reason={run.get('upgrade_reason')}"
                )
            verify = run.get("verify_result")
            if verify:
                lines.append(f"verify={json.dumps(verify, ensure_ascii=False)}")
            traces = run.get("traces", [])
            lines.append(f"trace_count={len(traces)}")
            for idx, step in enumerate(traces, start=1):
                lines.append(f"  - step{idx}:{step.get('tool')}")
                lines.append(f"    args={json.dumps(step.get('args', {}), ensure_ascii=False)}")
                lines.append(f"    result={json.dumps(step.get('result', {}), ensure_ascii=False)}")
        lines.append("")
    return "\n".join(lines).strip()

with st.sidebar:
    st.subheader("配置")
    kb_dir = st.text_input("知识库目录", value="kb")
    auto_upgrade = st.toggle("失败自动升级模型（flash-no -> pro-no）", value=True)
    base_url = st.text_input("OPENAI_BASE_URL", value=os.getenv("OPENAI_BASE_URL", ""))
    api_key = st.text_input("OPENAI_API_KEY", value=os.getenv("OPENAI_API_KEY", ""), type="password")
    primary_model = st.text_input("MODEL_PRIMARY", value=os.getenv("MODEL_PRIMARY", "gemini-3-flash-no"))
    fallback_model = st.text_input("MODEL_FALLBACK", value=os.getenv("MODEL_FALLBACK", "gemini-3-pro-no"))
    st.caption("此页面已使用真实工具调用循环，不再是 demo 规则编排。")

if base_url:
    os.environ["OPENAI_BASE_URL"] = base_url.strip()
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key.strip()
os.environ["MODEL_PRIMARY"] = primary_model.strip()
os.environ["MODEL_FALLBACK"] = fallback_model.strip()

engine = None
engine_error = None
try:
    engine = MCPToolExecutor(kb_dir=kb_dir)
except Exception as exc:  # noqa: BLE001
    engine_error = str(exc)
    st.error(f"配置未完成：{engine_error}")
    st.info("请在左侧补全 OPENAI_BASE_URL / OPENAI_API_KEY 后再提问。")


def run_prompt(prompt_text: str) -> None:
    if engine is None:
        st.warning("当前未完成模型配置，无法执行提问。")
        return
    st.session_state.history.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        latest_placeholder = st.empty()
        answer_placeholder = st.empty()
        trace_expander = st.expander("工具调用过程（透明可追溯）", expanded=True)
        trace_placeholder = trace_expander.empty()

        trace_log: list[dict] = []
        final_run = None
        for event in engine.run_stream(prompt=prompt_text, auto_upgrade=auto_upgrade):
            event_type = event.get("type")
            if event_type == "status":
                status_placeholder.info(event.get("message", "处理中..."))
            elif event_type == "tool_call":
                tool = event.get("tool")
                args = event.get("args", {})
                latest_placeholder.code(
                    f"正在调用工具: {tool}\n"
                    + json.dumps(args, ensure_ascii=False, indent=2),
                    language="json",
                )
            elif event_type == "tool_result":
                tool = event.get("tool")
                result = event.get("result", {})
                trace_log.append({"tool": tool, "result": result})
                latest_placeholder.code(
                    f"工具返回: {tool}\n"
                    + json.dumps(result, ensure_ascii=False, indent=2),
                    language="json",
                )
                trace_placeholder.code(json.dumps(trace_log, ensure_ascii=False, indent=2), language="json")
            elif event_type == "assistant_text":
                text = event.get("text", "")
                # Simulated token streaming for better UX.
                progressive = ""
                for ch in text:
                    progressive += ch
                    answer_placeholder.markdown(progressive)
            elif event_type == "final":
                final_run = event.get("run", {})

        if not final_run:
            status_placeholder.error("执行未返回最终结果。")
            return

        run = final_run
        st.session_state.last_run = run

        if run.get("upgraded"):
            st.info(
                f"已自动升级模型：`{run.get('primary_model')}` -> `{run.get('fallback_model')}` "
                f"(reason={run.get('upgrade_reason')})"
            )
        else:
            st.caption(f"本轮模型：`{run.get('model')}`")

        verify_result = run.get("verify_result")
        if verify_result:
            verify = verify_result.get("verify", {})
            if verify.get("ok"):
                st.success(f"自动验证通过，residual={verify.get('residual')}")
            else:
                st.error(f"自动验证未通过，residual={verify.get('residual')}")

        if not run.get("proof"):
            answer_placeholder.markdown("模型未返回文本结论，请查看工具调用过程。")
        else:
            answer_placeholder.markdown(run["proof"])

        with trace_expander:
            for idx, step in enumerate(run["traces"], start=1):
                st.markdown(f"**Step {idx}: `{step['tool']}`**")
                st.code(json.dumps(step["args"], ensure_ascii=False, indent=2), language="json")
                st.code(json.dumps(step["result"], ensure_ascii=False, indent=2), language="json")

    st.session_state.history.append(
        {
            "role": "assistant",
            "content": st.session_state.last_run.get("proof", ""),
            "run": st.session_state.last_run,
        }
    )


st.subheader("快速测试问题")
st.caption("点击任意按钮可直接提问，适合联调工具链。")
for i in range(0, len(TEST_QUESTIONS), 2):
    c1, c2 = st.columns(2)
    if c1.button(TEST_QUESTIONS[i], key=f"q_{i}", use_container_width=True):
        st.session_state.quick_prompt = TEST_QUESTIONS[i]
    if i + 1 < len(TEST_QUESTIONS):
        if c2.button(TEST_QUESTIONS[i + 1], key=f"q_{i+1}", use_container_width=True):
            st.session_state.quick_prompt = TEST_QUESTIONS[i + 1]

st.divider()
st.subheader("复制/导出")
export_text = _build_export_text(st.session_state.history)
c1, c2 = st.columns(2)
with c1:
    st.download_button(
        "下载全部输出（UTF-8 txt）",
        data=export_text.encode("utf-8"),
        file_name="math_agent_output.txt",
        mime="text/plain",
        use_container_width=True,
    )
with c2:
    st.caption("可在下方纯文本框中全选复制（UTF-8 不乱码）。")
with st.expander("纯文本预览（复制不乱码）", expanded=False):
    st.text_area("output_text", value=export_text, height=220)

for item in st.session_state.history:
    with st.chat_message(item["role"]):
        st.markdown(item["content"])
        run = item.get("run")
        if item.get("role") == "assistant" and isinstance(run, dict):
            verify = run.get("verify_result")
            if verify:
                detail = verify.get("verify", {})
                if detail.get("ok"):
                    st.caption(f"历史自动验证: 通过 (residual={detail.get('residual')})")
                else:
                    st.caption(f"历史自动验证: 未通过 (residual={detail.get('residual')})")
            with st.expander("工具调用过程（透明可追溯）", expanded=False):
                traces = run.get("traces", [])
                for idx, step in enumerate(traces, start=1):
                    st.markdown(f"**Step {idx}: `{step['tool']}`**")
                    st.code(json.dumps(step["args"], ensure_ascii=False, indent=2), language="json")
                    st.code(json.dumps(step["result"], ensure_ascii=False, indent=2), language="json")

typed_prompt = st.chat_input("输入数学/物理问题，例如：dy/dx=sin(x)")
quick_prompt = st.session_state.pop("quick_prompt", None) if "quick_prompt" in st.session_state else None
if quick_prompt:
    run_prompt(quick_prompt)
elif typed_prompt:
    run_prompt(typed_prompt)

st.divider()
st.subheader("验证按钮（兜底）")
if st.button("Verify 一键复验", use_container_width=True):
    if engine is None:
        st.warning("当前未完成模型配置，无法执行复验。")
        st.stop()
    if not st.session_state.last_run:
        st.warning("暂无可验证结果，请先运行一次问题。")
    else:
        verify = engine.verify_last(st.session_state.last_run)
        if not verify.get("ok"):
            st.warning(verify.get("reason", "复验失败"))
        else:
            payload = verify.get("verify", {})
            detail = payload.get("verify", {})
            if detail.get("ok"):
                st.success(f"复验通过，residual={detail.get('residual')}")
            else:
                st.error(f"复验未通过，residual={detail.get('residual')}")
            with st.expander("复验详情", expanded=False):
                st.code(json.dumps(verify, ensure_ascii=False, indent=2), language="json")

