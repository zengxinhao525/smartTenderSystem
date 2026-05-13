<script setup lang="ts">
const draft = defineModel<string>('draft', { required: true })

defineProps<{
  isResponding: boolean
  isUploading: boolean
}>()

defineEmits<{
  send: []
  upload: []
}>()
</script>

<template>
  <footer class="composer-wrap">
    <div class="composer">
      <textarea
        v-model="draft"
        class="composer__input"
        rows="1"
        placeholder="输入消息，Enter 发送，Shift + Enter 换行"
        @keydown.enter.exact.prevent="$emit('send')"
      />

      <div class="composer__actions">
        <span class="composer__hint">
          先上传 PDF 再追问细节，会更适合你的招投标场景
        </span>

        <div class="composer__buttons">
          <button class="ghost-action" type="button" @click="$emit('upload')">
            {{ isUploading ? '上传中...' : '上传文件' }}
          </button>
          <button
            class="send-button"
            type="button"
            :disabled="!draft.trim() || isResponding"
            @click="$emit('send')"
          >
            {{ isResponding ? '回复中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.composer-wrap {
  padding: 0 20px 24px;
}

.composer {
  width: min(900px, 100%);
  margin: 0 auto;
  padding: 18px;
  border-radius: 28px;
  background:
    linear-gradient(180deg, #ffffff, #fbfcfd);
  border: 1px solid #e6ecf3;
  box-shadow: 0 24px 50px rgba(29, 43, 61, 0.08);
}

.composer__input {
  width: 100%;
  min-height: 34px;
  resize: none;
  border: none;
  outline: none;
  background: transparent;
  color: #1b2b3d;
  font: inherit;
}

.composer__actions,
.composer__buttons {
  display: flex;
  align-items: center;
}

.composer__actions {
  justify-content: space-between;
  gap: 12px;
  margin-top: 12px;
}

.composer__buttons {
  gap: 10px;
}

.composer__hint {
  font-size: 12px;
  color: #738294;
}

.ghost-action,
.send-button {
  border: none;
  cursor: pointer;
  font: inherit;
}

.ghost-action {
  padding: 11px 16px;
  border-radius: 14px;
  color: #314255;
  background: #f3f5f8;
  border: 1px solid #e2e7ee;
}

.send-button {
  padding: 11px 18px;
  border-radius: 14px;
  color: white;
  background: linear-gradient(135deg, #2d80ff, #20b28f);
  font-weight: 700;
}

.send-button:disabled {
  cursor: not-allowed;
  opacity: 0.55;
}

@media (max-width: 960px) {
  .composer-wrap {
    padding: 0 14px 18px;
  }

  .composer__actions,
  .composer__buttons {
    width: 100%;
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
