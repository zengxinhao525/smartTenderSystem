<script setup lang="ts">
defineProps<{
  conversationTitle: string
  isUploading: boolean
  messageCountLabel: string
  modelLabel: string
}>()

defineEmits<{
  toggleSidebar: []
  upload: []
}>()
</script>

<template>
  <header class="topbar">
    <div class="topbar__title">
      <button class="menu-button" type="button" @click="$emit('toggleSidebar')">
        ☰
      </button>
      <div>
        <p class="eyebrow">Tender Workspace</p>
        <h1>{{ conversationTitle }}</h1>
      </div>
    </div>

    <div class="topbar__actions">
      <button class="upload-button" type="button" @click="$emit('upload')">
        {{ isUploading ? '解析中...' : '上传 PDF' }}
      </button>
      <span>{{ modelLabel }}</span>
      <span>{{ messageCountLabel }}</span>
    </div>
  </header>
</template>

<style scoped>
.topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 24px 28px 18px;
}

.topbar__title,
.topbar__actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.topbar__title h1 {
  margin: 4px 0 0;
  font-size: 24px;
  line-height: 1.1;
}

.eyebrow {
  margin: 0;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #8090a3;
}

.menu-button,
.upload-button {
  border: none;
  cursor: pointer;
  font: inherit;
}

.menu-button {
  display: none;
  width: 42px;
  height: 42px;
  border-radius: 14px;
  color: #3a4654;
  background: #f3f5f8;
}

.upload-button,
.topbar__actions span {
  padding: 8px 12px;
  border-radius: 999px;
  font-size: 12px;
}

.upload-button {
  color: #0d7f63;
  background: #eefaf6;
  border: 1px solid #cbeee3;
}

.topbar__actions span {
  color: #6f7d8c;
  background: #f3f5f8;
}

@media (max-width: 960px) {
  .topbar {
    padding: 18px 18px 14px;
  }

  .menu-button {
    display: inline-grid;
    place-items: center;
  }

  .topbar__actions {
    gap: 8px;
    flex-wrap: wrap;
    justify-content: flex-end;
  }
}
</style>
