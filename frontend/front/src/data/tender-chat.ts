import type { Conversation } from '@/types/tender-chat'

export const quickPrompts = [
  '帮我总结这份招标文件的核心要求',
  '请列出投标资格条件和截止时间',
  '把评分标准整理成表格思路',
  '给我一版更专业的投标答复框架',
]

export const conversationSeed: Conversation[] = [
  {
    id: 'conv-1',
    title: 'Vue 组件拆分建议',
    summary: '把大页面拆成 sidebar、message list 和 composer',
    model: 'GPT-4.1',
    messages: [
      {
        id: 'msg-1',
        role: 'assistant',
        content:
          '我们可以先把页面拆成三个稳定区域：左侧会话栏、中间消息流、底部输入区。这样后面接接口和做状态管理都会顺很多。',
        timestamp: '今天 09:18',
      },
    ],
  },
  {
    id: 'conv-2',
    title: '招标文件摘要',
    summary: '提取资格要求、评分项和截止时间',
    model: 'Qwen Plus',
    messages: [
      {
        id: 'msg-2',
        role: 'assistant',
        content:
          '如果你的目标是做智能招投标助手，前端建议重点突出三个动作：上传文件、快速提问、结构化结论卡片。',
        timestamp: '昨天 21:42',
      },
    ],
  },
]
