# 数学/物理证明 Agent 配置文档（Windows + WSL + micromamba）

本文档记录当前项目的完整配置流程，包含：
- Windows 主机环境
- WSL（Cadabra2）环境
- micromamba 环境与依赖
- API 配置
- Web 启停与常见问题

---

## 1. 项目路径

当前项目路径：

`C:\Users\kewei\Documents\2026\202602\16agent-proj`

建议后续保持该路径，避免再次重命名导致运行环境混淆。

---

## 2. Windows 主机配置（主执行环境）

### 2.1 创建 Python 环境

```powershell
mamba create -n math-agent-win python=3.11 pip -y
```

### 2.2 安装项目依赖

在项目根目录执行：

```powershell
micromamba run -n math-agent-win python -m pip install .
```

---

## 3. WSL 配置（Cadabra2）

Cadabra2 运行在 WSL 中，主机通过回退调用。

在 WSL 内执行：

```bash
micromamba create -n cadabra -c conda-forge --override-channels --strict-channel-priority --no-pin python=3.9 cadabra2 -y
```

验证：

```bash
micromamba run -n cadabra cadabra2
```

---

## 4. Mathematica 配置

自行到官网下载(https://www.wolfram.com/download-center/)最新版本，然后购买激活码即可。

安装后建议设置环境变量（Windows）：

```powershell
setx MATHEMATICA_BIN "C:\Program Files\Wolfram Research\Wolfram\14.3\wolframscript.exe"
```

验证：

```powershell
wolframscript -code "2+2"
```

---

## 5. API 配置（.env）

项目根目录的 `.env`（示例）：

```env
OPENAI_BASE_URL=https://hiapi.online/v1
OPENAI_API_KEY=你的key
MODEL_PRIMARY=gemini-3-flash-no
MODEL_FALLBACK=gemini-3-pro-no
CADABRA2_WSL_ENV=cadabra
```

说明：
- `OPENAI_BASE_URL` / `OPENAI_API_KEY` 也可在网页左侧手动输入
- `MODEL_PRIMARY` 失败会自动升级到 `MODEL_FALLBACK`

---

## 6. 启动与停止（推荐脚本）

### 6.1 推荐启动方式（固定端口）

```powershell
powershell -ExecutionPolicy Bypass -File scripts/start_webapp.ps1 -Port 8501
```

### 6.2 停止方式

```powershell
powershell -ExecutionPolicy Bypass -File scripts/stop_webapp.ps1 -Port 8501
```

该脚本会同时清理：
- `streamlit run src/math_agent_mcp/webapp.py` 对应 `python/micromamba` 进程树
- 指定端口的监听进程

---

## 7. 常见问题

### 7.1 Ctrl+C 后端口不断递增（8501 -> 8502 -> 8503...）

原因：旧 Streamlit 进程未完全释放。  
处理：优先使用上面的 start/stop 脚本，不建议直接多次手工 `streamlit run`。

### 7.2 看到 `WebSocketClosedError`

这是强制停止连接时的常见日志，一般可忽略。  
若频繁出现，先执行 `stop_webapp.ps1` 再 `start_webapp.ps1` 重启。

### 7.3 页面提示缺少 `OPENAI_BASE_URL` 或 `OPENAI_API_KEY`

检查：
1) `.env` 是否在项目根目录  
2) `.env` 是否已填入 key  
3) 网页左侧配置栏是否为空

---

## 8. 一次性自检命令

```powershell
micromamba run -n math-agent-win python scripts/gemini_smoke_test.py
micromamba run -n math-agent-win python scripts/toolchain_smoke_test.py
micromamba run -n math-agent-win python scripts/all_tools_question_test.py
```

全部通过后再进行复杂推导测试。
