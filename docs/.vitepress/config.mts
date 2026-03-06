import { defineConfig } from 'vitepress'

const isEdgeOne = process.env.EDGEONE === '1'
const baseConfig = isEdgeOne ? '/' : '/ace-claw/'

export default defineConfig({
  lang: 'zh-CN',
  title: 'OpenClaw 教程',
  description: 'OpenClaw 中文教程：本地部署、飞书接入、模型配置与高阶案例',
  base: baseConfig,
  markdown: {
    math: true
  },
  themeConfig: {
    logo: '/datawhale-logo.png',
    nav: [
      { text: '开始阅读', link: '/chapter1/chapter1' },
      { text: '环境配置', link: '/chapter3/' },
      { text: 'GitHub', link: 'https://github.com/datawhalechina/ace-claw' }
    ],
    search: {
      provider: 'local',
      options: {
        translations: {
          button: {
            buttonText: '搜索文档',
            buttonAriaLabel: '搜索文档'
          },
          modal: {
            noResultsText: '无法找到相关结果',
            resetButtonTitle: '清除查询条件',
            footer: {
              selectText: '选择',
              navigateText: '切换'
            }
          }
        }
      }
    },
    sidebar: [
      {
        text: '第一章 OpenClaw 概览',
        items: [
          { text: '1.1 OpenClaw 是什么', link: '/chapter1/chapter1' }
        ]
      },
      {
        text: '第二章 核心原理与系统架构',
        items: [
          { text: '2.1 系统组成与工作流', link: '/chapter2/chapter2_1' },
          { text: '2.2 模型与渠道配置思路', link: '/chapter2/chapter2_2' }
        ]
      },
      {
        text: '第三章 环境配置与基础上手',
        items: [
          { text: '3.1 Windows 本地部署与飞书接入', link: '/chapter3/' }
        ]
      },
      {
        text: '第四章 高阶案例',
        items: [
          { text: '4.1 数学与物理符号推理 Agent', link: '/chapter4/chapter4' }
        ]
      },
      {
        text: '第五章 生态扩展',
        items: [
          { text: '5.1 后续扩展路线', link: '/chapter5/' }
        ]
      }
    ],
    socialLinks: [
      { icon: 'github', link: 'https://github.com/datawhalechina/ace-claw' }
    ],
    editLink: {
      pattern: 'https://github.com/datawhalechina/ace-claw/blob/main/docs/:path'
    },
    footer: {
      message: '教程内容基于实际配置与排错过程整理，请结合 OpenClaw 官方文档交叉验证。',
      copyright:
        '文档默认采用 CC BY-NC-SA 4.0 协议共享。'
    }
  }
})
