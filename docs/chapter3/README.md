# 第三章 环境配置与基础上手

这一章的目标很明确：把 OpenClaw 在 Windows 本地环境里跑通，并完成飞书接入。

## 1. 建议先达到的最小目标

第一次配置时，不要同时追求所有能力。更合理的目标是先完成这四件事：

1. `openclaw` 命令可用
2. `openclaw gateway run` 能正常启动
3. Dashboard 能打开
4. 飞书私聊或群聊里能收到回复

只要这四步通了，后面的 skills、hooks、web search 才有意义。

## 2. Windows 本地部署建议

### 2.1 安装完成后先确认命令是否可用

如果安装后提示找不到 `openclaw`，高概率是 `Path` 没刷新或安装目录没进环境变量。

常见做法：

- 重新打开 PowerShell
- 检查安装目录是否在用户 `Path` 中
- 使用 `where.exe openclaw` 确认命令实际位置

### 2.2 日常不要反复跑 `onboard`

`openclaw onboard` 主要用于初始化和修改配置；平时真正运行应使用：

```bash
openclaw gateway run
```

然后用下面两条命令检查：

```bash
openclaw gateway probe
openclaw dashboard
```

## 3. 飞书接入的关键点

### 3.1 先把链路想清楚

飞书接入不只是填 `App ID` 和 `App Secret`。真正跑通需要四部分都成立：

- 飞书应用已创建
- 应用权限 scope 足够
- OpenClaw 中的飞书配置已写入
- 私聊配对或群聊策略已经放通

### 3.2 权限建议

基础消息场景下，至少要关注这几类权限：

- 即时消息相关权限
- 联系人读取相关权限
- 如果要操作云文档，再补充 doc/drive/wiki/bitable 相关权限

其中联系人权限是最容易漏掉但又会直接导致 pairing 或后续身份识别失败的一类。

### 3.3 pairing 的正确处理方式

如果飞书私聊出现 pairing code，不要只在聊天里回复“yes”。更稳的做法是在本机命令行里确认：

```bash
openclaw pairing list
openclaw pairing approve <code>
```

只有这里明确批准成功，私聊配对才算真正完成。

## 4. 模型配置建议

国内网络环境下，如果官方 OAuth 不稳定，更推荐用稳定的 OpenAI-compatible API。

建议优先满足这三点：

- `baseUrl` 正确
- `apiKey` 有效
- `model id` 已在 OpenClaw 中被设为默认模型

如果只是改了 provider，但默认模型还是旧配置，那么实际运行时仍然会报错。

## 5. 当前推荐的最小可用组合

如果你的目标是“先稳定用起来”，当前更推荐这套组合：

- 渠道：飞书 WebSocket
- 模型：OpenAI-compatible API
- 运行：`openclaw gateway run`
- 监测：`openclaw gateway probe`
- 配对：`openclaw pairing approve <code>`

## 6. 推荐阅读

这一章对应的详细长文教程位于仓库目录：

- `03环境配置与基础上手/01openclaw飞书安装.md`

如果你需要完整截图、逐步操作和排错记录，建议直接打开仓库中的这篇长文；本章更像是压缩后的主线版。
