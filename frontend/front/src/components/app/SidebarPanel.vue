<script setup lang="ts">
import type { Conversation } from '@/types/tender-chat'

defineProps<{
  activeConversationId: string
  conversations: Conversation[]
}>()

defineEmits<{
  createConversation: []
  selectConversation: [id: string]
}>()
</script>

<template>
  <aside class="sidebar">
    <div class="sidebar__top">
      <button class="sidebar__new" type="button" @click="$emit('createConversation')">
        <span>+</span>
        <span>新建对话</span>
      </button>

      <div class="sidebar__group">
        <p class="sidebar__label">最近对话</p>
        <div class="conversation-list">
          <button
            v-for="conversation in conversations"
            :key="conversation.id"
            class="conversation-card"
            :class="{
              'conversation-card--active': conversation.id === activeConversationId,
            }"
            type="button"
            @click="$emit('selectConversation', conversation.id)"
          >
            <strong>{{ conversation.title }}</strong>
            <span>{{ conversation.summary }}</span>
          </button>
        </div>
      </div>
    </div>

    <div class="workspace-card">
      <div class="workspace-card__avatar">ST</div>
      <div>
        <strong>smartTenderSystem</strong>
        <p>智能投标助手工作台</p>
      </div>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 296px;
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 22px 18px;
  background:
    linear-gradient(180deg, rgba(249, 250, 252, 0.96), rgba(244, 247, 251, 0.92));
  border-right: 1px solid #e6eaf0;
  backdrop-filter: blur(14px);
  overflow: hidden;
}

.sidebar__top,
.sidebar__group {
  display: flex;
  flex-direction: column;
}

.sidebar__top {
  min-height: 0;
  flex: 1;
  gap: 22px;
}

.sidebar__group {
  min-height: 0;
  flex: 1;
  gap: 12px;
}

.conversation-list {
  min-height: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding-right: 4px;
}

.sidebar__label {
  margin: 0 0 4px;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #7c8795;
}

.sidebar__new,
.conversation-card {
  border: none;
  cursor: pointer;
  font: inherit;
}

.sidebar__new {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 16px;
  border-radius: 18px;
  color: #ffffff;
  background: linear-gradient(135deg, #2d80ff, #20b28f);
  box-shadow: 0 14px 34px rgba(33, 104, 230, 0.28);
  font-weight: 700;
}

.conversation-card {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 14px;
  border-radius: 18px;
  text-align: left;
  color: #223041;
  background: #ffffff;
  border: 1px solid #e8edf3;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    background 0.18s ease;
}

.conversation-card:hover,
.conversation-card--active {
  transform: translateY(-1px);
  border-color: #bfd3f6;
  background: #f4f8ff;
}

.conversation-card strong,
.workspace-card strong {
  font-size: 14px;
}

.conversation-card span,
.workspace-card p {
  margin: 0;
  font-size: 12px;
  color: #728091;
}

.workspace-card {
  margin-top: 18px;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px;
  border-radius: 18px;
  background: #ffffff;
  border: 1px solid #e8edf3;
}

.workspace-card__avatar {
  width: 42px;
  height: 42px;
  display: grid;
  place-items: center;
  border-radius: 14px;
  font-weight: 700;
  color: white;
  background: linear-gradient(135deg, #ff9f43, #f55f44);
}
</style>
