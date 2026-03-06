---
layout: home

hero:
  name: "OpenClaw 教程"
  text: "从本地部署到飞书接入，再到垂直 Agent 落地"
  tagline: 面向真实使用场景整理的 OpenClaw 中文教程，不绕路，重点写清配置、排错和案例落地。
  image:
    src: /learning.GIF
    alt: OpenClaw 教程
  actions:
    - theme: brand
      text: 开始阅读
      link: /chapter1/chapter1
    - theme: alt
      text: 环境配置
      link: /chapter3/

features:
  - title: 跑通安装链路
    details: 覆盖 Windows 本地安装、网关启动、Dashboard 使用、pairing 配对与常见错误排查。
  - title: 讲清配置边界
    details: 把模型 provider、飞书权限、联系人 scope、hooks、skills 的作用和取舍讲清楚。
  - title: 提供可复用案例
    details: 除基础上手外，还整理了一个面向数学与物理推理任务的可验证 Agent 案例。
---

## 你会在这里看到什么

这套教程重点回答三个问题：

1. OpenClaw 到底适合做什么，不适合做什么
2. 如何在 Windows 环境里稳定跑通本地网关和飞书渠道
3. 跑通之后，怎样继续做出有实际价值的垂直 Agent

## 推荐阅读顺序

1. 第一章：先理解 OpenClaw 的定位、能力边界和适用场景
2. 第二章：看清网关、Agent、Skill、Provider、Channel 之间的关系
3. 第三章：按步骤完成安装和飞书联通
4. 第四章：参考一个真正的高阶 Agent 案例
5. 第五章：根据需要继续扩展搜索、技能、hooks 和更多渠道

## 使用建议

- 如果你是第一次接触 OpenClaw，先不要急着开 `skills` 和 `hooks`
- 如果你的目标只是让飞书机器人先回复消息，先把 `gateway`、`model`、`pairing` 这三步跑通
- 如果你在国内网络环境下使用，优先选择稳定的 OpenAI-compatible API
