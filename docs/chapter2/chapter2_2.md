# 第二章·续 模型与渠道配置思路

OpenClaw 真正容易卡住的地方，不在界面操作，而在“模型怎么接”“渠道怎么开”“错误该怎么看”。

## 1. 模型 provider 怎么选

理论上你有三种路：

1. 官方 OAuth
2. 自己维护的 provider 插件
3. OpenAI-compatible API

对于大多数中文用户，第三种最稳。原因很简单：

- 配置项少
- 不依赖额外插件
- 只要 `baseUrl + apiKey + model id` 正确，就能快速验证
- 出问题时更容易通过 `curl` 或脚本直接复测

因此，入门阶段建议优先选择一个稳定的 OpenAI-compatible 服务。

## 2. 模型配置的最小闭环

让 OpenClaw 能回消息，至少要确认这四件事：

- `baseUrl` 正确，且通常不能漏掉 `/v1`
- `apiKey` 有效，且账号有额度或权限
- `model id` 确实是 provider 支持的模型
- OpenClaw 的默认模型已经切换到该 provider，而不是还在走旧 fallback

如果只改了配置界面，但 `models status` 里默认模型没变，那说明系统实际上并没有用你以为的那套模型。

## 3. 飞书接入时最容易忽略的点

### 3.1 App ID / App Secret 不是全部

很多人填完 `App ID` 和 `App Secret`，就以为飞书接好了。实际上这只是“身份凭证”。

真正决定机器人能不能顺利工作的是：

- 是否开启了正确的事件订阅或长连接模式
- 是否把应用发布到当前企业
- 是否给了足够的权限 scope
- 私聊场景下是否完成了 pairing

### 3.2 联系人权限很关键

如果你看到飞书能收到消息，但机器人还是不回，或者日志里出现权限相关错误，那么高概率不是模型问题，而是飞书应用缺少联系人读取类权限。

这类问题很隐蔽，因为表面现象常常只是“机器人没反应”。

### 3.3 群聊策略要先想清楚

OpenClaw 在飞书里通常有几种策略：

- 仅私聊
- 群聊 allowlist
- 群聊 open，但要求 `@mention`

如果你只是想先测通，推荐直接选：

- 私聊先配对成功
- 群聊使用 `Open - respond in all groups (requires mention)`

这样排错最直接，避免被 allowlist 阻断。

## 4. 日常运行应该怎么做

初学阶段不建议把 OpenClaw 一上来就装成后台服务。更稳的方式是：

```bash
openclaw gateway run
```

保持这个窗口运行，然后在另一个窗口里检查：

```bash
openclaw gateway probe
openclaw dashboard
```

这比反复执行 `openclaw onboard` 更适合日常使用，因为：

- `onboard` 是向导，不是常驻服务
- `gateway run` 更接近真实运行状态
- 问题出现时日志也更容易直接观察

## 5. 推荐的排错顺序

遇到“不回消息”“Dashboard 报错”“看起来配好了但没反应”时，建议按这个顺序排：

1. 先确认网关在不在：`openclaw gateway probe`
2. 再看模型是否真在用当前 provider：`openclaw models status --json`
3. 然后看飞书通道状态：`openclaw channels status --probe`
4. 私聊场景再查 pairing：`openclaw pairing list`
5. 最后看日志里有没有权限、401、403 或 provider 错误

这个顺序能避免你在错误的方向上重复折腾。
