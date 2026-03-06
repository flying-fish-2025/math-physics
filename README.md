# OpenClaw 教程

> [!WARNING]
> 当前仓库已整理为可直接阅读和发布的版本，但 OpenClaw 本身迭代较快。若官方命令、配置项或安全建议发生变化，请以官方文档为准，并同步更新本仓库。

这是一个围绕 **OpenClaw 自托管 AI 助手平台** 的中文教程仓库，目标不是简单复述官方文档，而是把真正会踩坑的安装、权限、模型接入、案例落地过程整理成一套可复用的学习路径。

本仓库覆盖三类内容：

- OpenClaw 的产品定位、核心架构与使用边界
- Windows 本地部署、飞书接入、模型 provider 配置与排错
- 一个面向数学与物理符号推理任务的高阶 Agent 案例

## 适合谁看

1. 希望把 OpenClaw 跑起来并接入飞书、Slack 等渠道的开发者
2. 想基于 OpenClaw 做垂直 Agent、工具链集成或自动化工作流的人
3. 需要一个完整开源案例来理解 Skill、MCP、外部工具协同方式的学习者

## 在线阅读

- 文档站：首页构建后可直接通过 VitePress 浏览
- 本地预览：

```bash
npm install
npm run docs:dev
```

## 仓库结构

| 路径 | 说明 |
| ---- | ---- |
| `docs/` | VitePress 在线文档站 |
| `03环境配置与基础上手/` | 安装和飞书接入的原始长文教程与配图 |
| `16agent-proj/` | 数学/物理符号推理 Agent 案例工程 |

## 教程目录

| 章节 | 内容 | 状态 |
| ---- | ---- | ---- |
| [第一章 OpenClaw 概览](./docs/chapter1/chapter1.md) | OpenClaw 的定位、核心能力、适用场景与风险边界 | 已完成 |
| [第二章 核心原理与系统架构](./docs/chapter2/chapter2_1.md) | 网关、Agent、Channel、Skill、Provider 等核心概念 | 已完成 |
| [第二章·续 模型与渠道配置思路](./docs/chapter2/chapter2_2.md) | 模型 provider 选择、飞书接入策略、常见错误定位 | 已完成 |
| [第三章 环境配置与基础上手](./docs/chapter3/README.md) | Windows 本地部署、飞书安装、pairing 与日常运行方式 | 已完成 |
| [第四章 高阶案例：数学与物理符号推理 Agent](./docs/chapter4/chapter4.md) | OpenClaw 之外，如何设计一个低幻觉的可验证 Agent 案例 | 已完成 |
| [第五章 生态扩展与后续路线](./docs/chapter5/README.md) | 如何继续扩展 skills、hooks、web search 与更多渠道 | 已完成 |

## 推荐阅读顺序

1. 先看 [第一章](./docs/chapter1/chapter1.md) 和 [第二章](./docs/chapter2/chapter2_1.md)，建立对 OpenClaw 的整体认识
2. 再看 [第三章](./docs/chapter3/README.md)，按步骤完成安装、模型接入和飞书联通
3. 跑通基础环境后，再进入 [第四章](./docs/chapter4/chapter4.md) 看一个完整案例如何落地
4. 最后根据需求阅读 [第五章](./docs/chapter5/README.md)，决定是否继续扩展 hooks、skills、web search 等能力

## 当前推荐配置

如果你的目标是先稳定跑通 OpenClaw，而不是折腾官方 OAuth 或自建 provider，当前更推荐这套组合：

- 渠道：飞书 WebSocket
- 模型：OpenAI-compatible provider
- 运行：`openclaw gateway run`
- 控制台：`openclaw dashboard`
- 配对：`openclaw pairing approve <code>`

对于国内网络环境，建议优先使用一个稳定可用的 OpenAI-compatible API，再接入 OpenClaw，而不是把时间耗在不可用的 OAuth 流程上。

## 相关资料

- 原始飞书安装长文：[01openclaw飞书安装.md](./03环境配置与基础上手/01openclaw飞书安装.md)
- 案例工程说明：[16agent-proj/README.md](./16agent-proj/README.md)
- 案例环境配置：[16agent-proj/docs/CONFIG_SETUP_CN.md](./16agent-proj/docs/CONFIG_SETUP_CN.md)

## 参与贡献

- 如果你发现教程步骤失效、命令变化或截图与当前版本不一致，直接提 Issue 即可
- 如果你有新的 OpenClaw 案例，建议补充最少三部分内容：目标问题、配置步骤、排错记录
- 如果你准备提交 PR，优先保证内容能被读者直接复现，而不是只给结论

## 贡献者名单

| 姓名   | 职责           | 简介               |
| ------ | -------------- | ------------------ |
| 肖泽华 | 项目负责人 | 数学物理研究者     |
| 龙垭宇 | 第1、2章贡献者 | 机器学习在读研究生 |
| 肖泽华 | 第3、4章贡献者 | 数学物理研究者     |
| 陈可为 | 第5章贡献者    | 机器学习在读研究生 |

## 参与贡献

- 如果你发现了一些问题，可以提Issue进行反馈，如果提完没有人回复你可以联系[保姆团队](https://github.com/datawhalechina/DOPMC/blob/main/OP.md)的同学进行反馈跟进~
- 如果你想参与贡献本项目，可以提Pull Request，如果提完没有人回复你可以联系[保姆团队](https://github.com/datawhalechina/DOPMC/blob/main/OP.md)的同学进行反馈跟进~
- 如果你对 Datawhale 很感兴趣并想要发起一个新的项目，请按照[Datawhale开源项目指南](https://github.com/datawhalechina/DOPMC/blob/main/GUIDE.md)进行操作即可~

## 关注我们

扫描下方二维码关注公众号：Datawhale

[![img](https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg)](https://raw.githubusercontent.com/datawhalechina/pumpkin-book/master/res/qrcode.jpeg)

## LICENSE

[![知识共享许可协议](https://camo.githubusercontent.com/4e651249bcd5e4a919f8b85221435dc46c5f70de051ec49d4ebe0f61bfd7f72a/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f6c6963656e73652d434325323042592d2d4e432d2d5341253230342e302d6c6967687467726579)](http://creativecommons.org/licenses/by-nc-sa/4.0/)
本作品采用[知识共享署名-非商业性使用-相同方式共享 4.0 国际许可协议](http://creativecommons.org/licenses/by-nc-sa/4.0/)进行许可。


