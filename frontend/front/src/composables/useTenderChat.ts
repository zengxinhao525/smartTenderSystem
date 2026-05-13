import { computed, nextTick, ref, watch, type Ref } from 'vue'

import { conversationSeed } from '@/data/tender-chat'
import type {
  ChatApiMessage,
  ChatApiResponse,
  Conversation,
  Message,
  Role,
  UploadAnalysisResponse,
} from '@/types/tender-chat'

const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000'
).replace(/\/$/, '')

export function useTenderChat(messageViewport: Ref<HTMLElement | null>) {
  const conversations = ref<Conversation[]>(conversationSeed)
  const activeConversationId = ref(conversationSeed[0]?.id ?? '')
  const draft = ref('')
  const isResponding = ref(false)
  const isUploading = ref(false)
  const sidebarOpen = ref(true)
  const errorMessage = ref('')
  const latestAnalysis = ref<UploadAnalysisResponse | null>(null)

  const activeConversation = computed(() =>
    conversations.value.find((item) => item.id === activeConversationId.value),
  )

  const messageCountLabel = computed(() => {
    const count = activeConversation.value?.messages.length ?? 0
    return `${count} 条消息`
  })

  function createId(prefix: string) {
    return `${prefix}-${Date.now()}-${Math.random().toString(16).slice(2, 8)}`
  }

  function createConversation() {
    const conversation: Conversation = {
      id: createId('conv'),
      title: '新的对话',
      summary: '从这里开始输入你的问题',
      model: 'GPT-4.1',
      messages: [],
    }

    conversations.value = [conversation, ...conversations.value]
    activeConversationId.value = conversation.id
    draft.value = ''
    errorMessage.value = ''
    latestAnalysis.value = null
  }

  function selectConversation(id: string) {
    activeConversationId.value = id
    errorMessage.value = ''

    if (window.innerWidth <= 960) {
      sidebarOpen.value = false
    }
  }

  function appendMessage(role: Role, content: string) {
    const targetConversation = activeConversation.value
    if (!targetConversation) return

    targetConversation.messages.push({
      id: createId('msg'),
      role,
      content,
      timestamp: new Intl.DateTimeFormat('zh-CN', {
        hour: '2-digit',
        minute: '2-digit',
      }).format(new Date()),
    })

    if (role === 'user') {
      targetConversation.title = content.slice(0, 14) || '新的对话'
      targetConversation.summary = content.slice(0, 28) || '等待新的回复'
    } else {
      targetConversation.summary = content.slice(0, 28)
    }
  }

  function buildChatHistory(messages: Message[]): ChatApiMessage[] {
    return messages.map((message) => ({
      role: message.role,
      content: message.content,
    }))
  }

  function createAnalysisSummary(result: UploadAnalysisResponse) {
    const bidInfo = result.bid_info || {}
    const requirements = (bidInfo.technical_requirements || []).slice(0, 4)
    const requirementText = requirements.length
      ? requirements.map((item, index) => `${index + 1}. ${item}`).join('\n')
      : '暂未抽取到明确的技术要求。'

    return [
      `我已经完成对文件《${result.file_name}》的初步解析。`,
      '',
      `项目名称：${bidInfo.project_name || '未识别'}`,
      `截止时间：${bidInfo.deadline || '未识别'}`,
      '',
      '技术要求摘录：',
      requirementText,
      '',
      `自动审查结论：${result.review || '暂无审查结果'}`,
      result.need_human
        ? '当前流程建议继续人工审核。'
        : '当前流程暂不需要额外人工审核。',
    ].join('\n')
  }

  async function scrollToBottom() {
    await nextTick()
    const viewport = messageViewport.value
    if (!viewport) return
    viewport.scrollTop = viewport.scrollHeight
  }

  async function submitMessage() {
    const content = draft.value.trim()
    if (!content || isResponding.value) return

    errorMessage.value = ''

    const targetConversation = activeConversation.value
    if (!targetConversation) return

    appendMessage('user', content)
    draft.value = ''
    isResponding.value = true
    await scrollToBottom()

    try {
      const response = await fetch(`${apiBaseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: content,
          history: buildChatHistory(targetConversation.messages.slice(0, -1)),
        }),
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = (await response.json()) as ChatApiResponse
      appendMessage('assistant', data.reply)
      targetConversation.model = data.model || targetConversation.model

      if (data.fallback) {
        targetConversation.summary = '当前使用后端兜底回复'
      }
    } catch (error) {
      errorMessage.value =
        '暂时无法连接后端聊天接口，请确认后端服务已经启动，并检查地址配置。'
      appendMessage(
        'assistant',
        '当前没有成功连接到后端聊天服务，所以这条回复是前端错误提示。你可以先启动后端，再继续对话。',
      )
      console.error(error)
    } finally {
      isResponding.value = false
      await scrollToBottom()
    }
  }

  async function uploadFile(file: File) {
    if (isUploading.value) return

    errorMessage.value = ''
    isUploading.value = true

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch(`${apiBaseUrl}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }

      const data = (await response.json()) as UploadAnalysisResponse
      latestAnalysis.value = data
      appendMessage('assistant', createAnalysisSummary(data))
      await scrollToBottom()
    } catch (error) {
      errorMessage.value =
        '文件上传或解析失败，请确认后端服务已启动，并且上传的是 PDF 文件。'
      console.error(error)
    } finally {
      isUploading.value = false
    }
  }

  function sendPrompt(prompt: string) {
    draft.value = prompt
    void submitMessage()
  }

  watch(activeConversationId, async () => {
    await scrollToBottom()
  })

  return {
    activeConversation,
    activeConversationId,
    apiBaseUrl,
    conversations,
    createConversation,
    draft,
    errorMessage,
    isResponding,
    isUploading,
    latestAnalysis,
    messageCountLabel,
    scrollToBottom,
    sendPrompt,
    selectConversation,
    sidebarOpen,
    submitMessage,
    uploadFile,
  }
}
