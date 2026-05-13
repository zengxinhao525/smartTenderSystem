<script setup lang="ts">
import type { UploadAnalysisResponse } from '@/types/tender-chat'

defineProps<{
  analysis: UploadAnalysisResponse
}>()
</script>

<template>
  <section class="analysis-panel">
    <div class="analysis-panel__header">
      <div>
        <p class="eyebrow">文件解析结果</p>
        <h3>{{ analysis.file_name }}</h3>
      </div>

      <span
        class="analysis-badge"
        :class="{ 'analysis-badge--warn': analysis.need_human }"
      >
        {{ analysis.need_human ? '待人工复核' : '已完成初筛' }}
      </span>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <strong>项目名称</strong>
        <p>{{ analysis.bid_info.project_name || '未识别' }}</p>
      </article>
      <article class="analysis-card">
        <strong>截止时间</strong>
        <p>{{ analysis.bid_info.deadline || '未识别' }}</p>
      </article>
      <article class="analysis-card analysis-card--wide">
        <strong>文档摘要</strong>
        <p>{{ analysis.bid_info.summary || '暂无摘要' }}</p>
      </article>
      <article class="analysis-card analysis-card--wide">
        <strong>自动审查</strong>
        <p>{{ analysis.review || '暂无结果' }}</p>
      </article>
    </div>
  </section>
</template>

<style scoped>
.analysis-panel {
  width: min(900px, 100%);
  margin: 0 auto 18px;
  padding: 20px;
  border-radius: 28px;
  background:
    linear-gradient(180deg, #ffffff, #fbfcfd);
  border: 1px solid #e7edf4;
  box-shadow: 0 18px 36px rgba(21, 33, 52, 0.06);
}

.analysis-panel__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.analysis-panel__header h3 {
  margin: 6px 0 0;
  font-size: 20px;
}

.eyebrow {
  margin: 0;
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #8090a3;
}

.analysis-badge {
  padding: 8px 12px;
  border-radius: 999px;
  background: #eefaf4;
  color: #177957;
  font-size: 12px;
}

.analysis-badge--warn {
  background: #fff6e7;
  color: #a96a04;
}

.analysis-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}

.analysis-card {
  padding: 16px;
  border-radius: 20px;
  background: #f8fafc;
  border: 1px solid #edf1f5;
}

.analysis-card--wide {
  grid-column: 1 / -1;
}

.analysis-card strong {
  display: block;
  margin-bottom: 8px;
  font-size: 13px;
}

.analysis-card p {
  margin: 0;
  color: #314255;
  line-height: 1.7;
  white-space: pre-wrap;
}

@media (max-width: 960px) {
  .analysis-grid {
    grid-template-columns: 1fr;
  }

  .analysis-panel__header {
    flex-direction: column;
  }
}
</style>
