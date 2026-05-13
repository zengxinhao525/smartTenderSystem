<script setup lang="ts">
import { ref } from 'vue'

import AnalysisPanel from '@/components/app/AnalysisPanel.vue'
import ComposerPanel from '@/components/app/ComposerPanel.vue'
import EmptyState from '@/components/app/EmptyState.vue'
import ErrorBanner from '@/components/app/ErrorBanner.vue'
import MessageList from '@/components/app/MessageList.vue'
import SidebarPanel from '@/components/app/SidebarPanel.vue'
import TopBar from '@/components/app/TopBar.vue'
import { quickPrompts } from '@/data/tender-chat'
import { useTenderChat } from '@/composables/useTenderChat'

const fileInput = ref<HTMLInputElement | null>(null)
const messageViewport = ref<HTMLElement | null>(null)

const {
  activeConversation,
  activeConversationId,
  conversations,
  createConversation,
  draft,
  errorMessage,
  isResponding,
  isUploading,
  latestAnalysis,
  messageCountLabel,
  sendPrompt,
  selectConversation,
  sidebarOpen,
  submitMessage,
  uploadFile,
} = useTenderChat(messageViewport)

function openFilePicker() {
  fileInput.value?.click()
}

async function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return

  await uploadFile(file)
  target.value = ''
}
</script>

<template>
  <div class="app-shell">
    <aside class="sidebar-frame" :class="{ 'sidebar-frame--open': sidebarOpen }">
      <SidebarPanel
        :active-conversation-id="activeConversationId"
        :conversations="conversations"
        @create-conversation="createConversation"
        @select-conversation="selectConversation"
      />
    </aside>

    <div
      v-if="sidebarOpen"
      class="sidebar-backdrop"
      @click="sidebarOpen = false"
    />

    <main class="main-panel">
      <TopBar
        :conversation-title="activeConversation?.title ?? '新的对话'"
        :is-uploading="isUploading"
        :message-count-label="messageCountLabel"
        :model-label="activeConversation?.model ?? 'GPT-4.1'"
        @toggle-sidebar="sidebarOpen = !sidebarOpen"
        @upload="openFilePicker"
      />

      <section ref="messageViewport" class="message-viewport">
        <input
          ref="fileInput"
          class="sr-only"
          type="file"
          accept=".pdf,application/pdf"
          @change="handleFileChange"
        >

        <ErrorBanner v-if="errorMessage" :message="errorMessage" />
        <AnalysisPanel v-if="latestAnalysis" :analysis="latestAnalysis" />

        <EmptyState
          v-if="!(activeConversation?.messages.length)"
          :prompts="quickPrompts"
          @send-prompt="sendPrompt"
        />

        <MessageList
          v-else
          :is-responding="isResponding"
          :messages="activeConversation.messages"
        />
      </section>

      <ComposerPanel
        v-model:draft="draft"
        :is-responding="isResponding"
        :is-uploading="isUploading"
        @send="submitMessage"
        @upload="openFilePicker"
      />
    </main>
  </div>
</template>

<style scoped>
:global(*) {
  box-sizing: border-box;
}

:global(body) {
  margin: 0;
  font-family:
    "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei",
    sans-serif;
  color: #16202b;
  background:
    radial-gradient(circle at top, rgba(82, 140, 255, 0.12), transparent 30%),
    linear-gradient(180deg, #ffffff 0%, #f6f8fb 100%);
}

:global(html) {
  scrollbar-width: thin;
  scrollbar-color: #c8ced8 transparent;
}

:global(*::-webkit-scrollbar) {
  width: 8px;
  height: 8px;
}

:global(*::-webkit-scrollbar-track) {
  background: transparent;
}

:global(*::-webkit-scrollbar-thumb) {
  border-radius: 999px;
  background: #c8ced8;
  border: 2px solid transparent;
  background-clip: padding-box;
}

:global(*::-webkit-scrollbar-thumb:hover) {
  background: #b3bbc7;
  border: 2px solid transparent;
  background-clip: padding-box;
}

#app {
  height: 100vh;
}

.app-shell {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar-frame {
  flex-shrink: 0;
  height: 100vh;
}

.main-panel {
  flex: 1;
  height: 100vh;
  min-width: 0;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background:
    radial-gradient(circle at top, rgba(70, 130, 255, 0.08), transparent 34%),
    linear-gradient(180deg, #ffffff 0%, #f7f9fc 100%);
}

.message-viewport {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 0 28px 24px;
  scroll-behavior: smooth;
}

.sr-only {
  display: none;
}

.sidebar-backdrop {
  display: none;
}

@media (max-width: 960px) {
  .sidebar-frame {
    position: fixed;
    top: 0;
    left: 0;
    bottom: 0;
    transform: translateX(-100%);
    transition: transform 0.24s ease;
    z-index: 20;
  }

  .sidebar-frame--open {
    transform: translateX(0);
  }

  .sidebar-backdrop {
    display: block;
    position: fixed;
    inset: 0;
    background: rgba(25, 32, 43, 0.12);
    backdrop-filter: blur(3px);
    z-index: 10;
  }

  .message-viewport {
    padding: 0 18px 18px;
  }
}
</style>
