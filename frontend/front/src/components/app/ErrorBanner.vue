<script setup lang="ts">
defineProps<{
  message: string
}>()
</script>

<template>
  <div class="error-banner">{{ message }}</div>
</template>

<style scoped>
.error-banner {
  width: min(900px, 100%);
  margin: 0 auto 16px;
  padding: 12px 14px;
  border-radius: 18px;
  color: #ffd6d6;
  background: rgba(212, 82, 82, 0.16);
  border: 1px solid rgba(255, 135, 135, 0.22);
  font-size: 13px;
}
</style>
