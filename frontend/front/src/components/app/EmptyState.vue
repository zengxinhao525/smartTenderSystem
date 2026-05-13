<script setup lang="ts">
defineProps<{
  prompts: string[]
}>()

defineEmits<{
  sendPrompt: [prompt: string]
}>()
</script>

<template>
  <section class="empty-state">
    <p class="eyebrow">Upload First, Then Ask</p>
    <h2>把招标文件交给它，先解析，再继续追问</h2>
    <p class="empty-state__text">
      页面已经支持真实聊天和 PDF 解析。更适合的使用方式是先上传文档，让系统抽取关键信息，再围绕结果持续对话。
    </p>

    <div class="prompt-grid">
      <button
        v-for="prompt in prompts"
        :key="prompt"
        class="prompt-card"
        type="button"
        @click="$emit('sendPrompt', prompt)"
      >
        {{ prompt }}
      </button>
    </div>
  </section>
</template>

<style scoped>
.empty-state {
  width: min(900px, 100%);
  margin: 0 auto;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 42px 0 24px;
}

.eyebrow {
  margin: 0;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #8090a3;
}

.empty-state h2 {
  margin: 8px 0 12px;
  max-width: 720px;
  font-size: clamp(30px, 5vw, 52px);
  line-height: 1.04;
}

.empty-state__text {
  max-width: 640px;
  margin: 0;
  color: #66788c;
  line-height: 1.8;
}

.prompt-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin-top: 28px;
}

.prompt-card {
  padding: 18px;
  border: 1px solid #e8edf3;
  border-radius: 22px;
  text-align: left;
  color: #203042;
  background:
    linear-gradient(180deg, #ffffff, #f8fafc);
  cursor: pointer;
  font: inherit;
  transition:
    transform 0.18s ease,
    border-color 0.18s ease,
    box-shadow 0.18s ease;
}

.prompt-card:hover {
  transform: translateY(-2px);
  border-color: #c7d8f7;
  box-shadow: 0 18px 30px rgba(39, 55, 79, 0.08);
}

@media (max-width: 960px) {
  .prompt-grid {
    grid-template-columns: 1fr;
  }
}
</style>
