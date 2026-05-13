<script setup lang="ts">
import type { Message } from '@/types/tender-chat'

defineProps<{
  isResponding: boolean
  messages: Message[]
}>()
</script>

<template>
  <section class="message-list">
    <article
      v-for="message in messages"
      :key="message.id"
      class="message-row"
      :class="`message-row--${message.role}`"
    >
      <div class="avatar">
        {{ message.role === 'assistant' ? 'AI' : '你' }}
      </div>

      <div class="bubble">
        <div class="bubble__meta">
          <strong>{{ message.role === 'assistant' ? 'SmartTender AI' : '你' }}</strong>
          <span>{{ message.timestamp }}</span>
        </div>
        <p>{{ message.content }}</p>
      </div>
    </article>

    <article v-if="isResponding" class="message-row">
      <div class="avatar">AI</div>
      <div class="bubble bubble--typing">
        <div class="bubble__meta">
          <strong>SmartTender AI</strong>
          <span>正在输入</span>
        </div>
        <div class="typing-dots">
          <span />
          <span />
          <span />
        </div>
      </div>
    </article>
  </section>
</template>

<style scoped>
.message-list {
  width: min(900px, 100%);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 18px;
  padding-top: 8px;
}

.message-row {
  display: flex;
  gap: 14px;
  align-items: flex-start;
}

.message-row--user {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  display: grid;
  place-items: center;
  border-radius: 14px;
  font-weight: 700;
  color: #ffffff;
  background: linear-gradient(135deg, #2d80ff, #25466e);
}

.message-row--user .avatar {
  background: linear-gradient(135deg, #16b899, #2276bd);
}

.bubble {
  max-width: min(720px, 100%);
  padding: 16px 18px;
  border-radius: 24px;
  color: #213144;
  background: #ffffff;
  border: 1px solid #e8edf3;
  box-shadow: 0 16px 36px rgba(36, 49, 68, 0.06);
}

.message-row--user .bubble {
  color: white;
  background: linear-gradient(135deg, rgba(18, 166, 143, 0.92), rgba(37, 108, 199, 0.92));
}

.bubble__meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 8px;
}

.bubble__meta strong {
  font-size: 14px;
}

.bubble__meta span {
  font-size: 12px;
  color: #7d8ea0;
}

.bubble p {
  margin: 0;
  white-space: pre-wrap;
  line-height: 1.72;
}

.bubble--typing {
  min-width: 180px;
}

.typing-dots {
  display: inline-flex;
  gap: 8px;
  padding-top: 6px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 999px;
  background: #dbe9f7;
  animation: blink 1.1s infinite ease-in-out;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.16s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.32s;
}

@keyframes blink {
  0%,
  80%,
  100% {
    transform: translateY(0);
    opacity: 0.35;
  }

  40% {
    transform: translateY(-2px);
    opacity: 1;
  }
}
</style>
