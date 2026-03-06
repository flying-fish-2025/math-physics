# 第四章 高阶案例：数学与物理符号推理 Agent

这一章不再停留在 OpenClaw 安装层，而是回答另一个更重要的问题：**当基础平台跑通之后，怎样设计一个真正可靠的垂直 Agent。**

本章案例对应仓库中的 `16agent-proj/` 目录，目标是构建一个面向数学与物理推导任务的低幻觉 Agent。

## 1. 为什么要做这个案例

数学证明、公式推导、符号变换这类任务对“正确性”的要求远高于普通问答。单纯依赖大模型直接生成，常见问题包括：

- 跳步
- 乱用恒等式
- 微分方程求解过程不严谨
- 最终结果看起来像对的，但无法验证

所以这个案例的设计原则是：**让 LLM 负责决策与编排，让可验证工具负责计算与校验。**

## 2. 核心设计思路

### 2.1 MCP 管正确性

MCP 层承接所有需要结构化和可追溯的计算动作，例如：

- 定义符号
- 构造表达式
- 化简与替换
- 微分方程求解
- 最终代回验证

### 2.2 Skill 管方法论

Skill 的作用不是替代工具，而是约束模型行为，例如：

- 不允许跳步
- 不允许心算关键结果
- 每一步都要引用工具返回值
- 最后必须做验证

一句话总结就是：**MCP 管正确性，Skill 管流程纪律。**

## 3. 项目结构

案例工程中的关键模块包括：

- `src/math_agent_mcp/session_manager.py`：会话状态与对象仓库
- `src/math_agent_mcp/tools/`：SymPy、Cadabra2、Mathematica、知识库适配层
- `src/math_agent_mcp/mcp_server.py`：Stateful MCP Server
- `src/math_agent_mcp/mcp_tool_executor.py`：LLM 工具调用执行器
- `src/math_agent_mcp/webapp.py`：前端交互界面

这套结构的优点是职责清晰：工具负责执行，执行器负责调度，会话管理负责跨轮状态。

## 4. 为什么这个案例值得参考

即使你的目标不是数学或物理推导，这个案例仍然有很强的参考价值，因为它展示了一个通用模式：

1. 先识别高风险任务里哪些部分不能交给模型“猜”
2. 把这些部分抽成工具接口
3. 让模型只负责选择工具、组织步骤和整合结果
4. 在最终输出前做独立验证

这个模式可以迁移到很多领域，例如：

- 财务计算
- 合同规则检查
- 数据处理流程
- 工程公式计算

## 5. 快速开始

完整环境配置见仓库中的以下文件：

- `16agent-proj/README.md`
- `16agent-proj/docs/CONFIG_SETUP_CN.md`

最小启动流程如下：

```bash
mamba create -n math-agent-win python=3.11 pip -y
micromamba run -n math-agent-win python -m pip install .
micromamba run -n math-agent-win python -m math_agent_mcp.mcp_server
micromamba run -n math-agent-win streamlit run src/math_agent_mcp/webapp.py
```

## 6. 这和 OpenClaw 的关系是什么

这个案例不是“OpenClaw 官方插件”，而是一个很好的思路延展：

- OpenClaw 负责消息入口、Agent 运行平台和整体协作框架
- 垂直案例负责领域能力、工具接入和正确性控制

如果你未来准备做自己的专业助手，真正重要的不是把聊天界面做漂亮，而是像这个案例一样，把“哪些事必须可验证”拆出来。

## 7. 下一步建议

如果你已经看完前三章并跑通了 OpenClaw，可以从这个案例继续往下走：

1. 先把一个你自己的专业任务拆成“模型负责什么，工具负责什么”
2. 不要一开始就追求全自动，先做一个能验证的小闭环
3. 把成功案例沉淀成 Skill、Tool 或独立项目，而不是只留在聊天记录里
