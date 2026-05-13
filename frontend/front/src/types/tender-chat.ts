export type Role = 'user' | 'assistant'

export interface Message {
  id: string
  role: Role
  content: string
  timestamp: string
}

export interface Conversation {
  id: string
  title: string
  summary: string
  model: string
  messages: Message[]
}

export interface ChatApiMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface ChatApiResponse {
  reply: string
  model: string
  fallback: boolean
}

export interface UploadAnalysisResponse {
  file_name: string
  file_path: string
  bid_info: {
    project_name?: string
    deadline?: string
    technical_requirements?: string[]
    summary?: string
  }
  draft: string
  review: string
  approved: boolean
  need_human: boolean
}
