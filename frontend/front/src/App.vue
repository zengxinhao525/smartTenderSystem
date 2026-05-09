<template>
  <div class="gpt-layout">
    <!-- 1. 左侧侧边栏 (历史记录) -->
    <aside class="sidebar">
      <div class="new-chat-btn">
        + 新建对话
      </div>

      <div class="history-list">
        <!-- 模拟的历史记录 -->
        <div class="history-item">前端代码优化建议</div>
        <div class="history-item">Vue3 生命周期详解</div>
        <div class="history-item">CSS Flex 布局教程</div>
        <!-- 这里以后会替换成 v-for 循环 -->
      </div>

      <div class="user-menu">
        用户设置
      </div>
    </aside>

    <!-- 2. 右侧主内容区 -->
    <main class="main-content">
      <!-- 顶部导航 (可选) -->
      <header class="top-bar">
        <span>GPT-4.0</span>
      </header>

      <!-- 核心滚动区域：聊天记录 -->
      <div class="chat-container">
        <!-- 这里的 router-view 会显示你的 views/Home.vue 或 views/Chat.vue -->
        <router-view />
      </div>

      <!-- 底部输入框区域 (如果想固定在底部，也可以放在 router-view 外面) -->
      <!-- <div class="input-area">
        <input type="text" placeholder="发送消息..." />
      </div> -->
    </main>
  </div>
</template>

<script setup lang="ts">
// 这里可以写侧边栏的折叠逻辑
</script>

<style scoped>
/* 整体布局：左右结构，占满全屏 */
.gpt-layout {
  display: flex;
  width: 100vw;
  height: 100vh;
  background-color: #ffffff; /* 主背景白 */
  overflow: hidden; /* 防止整个页面滚动 */
}

/* --- 左侧侧边栏 --- */
.sidebar {
  width: 260px; /* 固定宽度 */
  background-color: #f7f7f8; /* ChatGPT 经典的浅灰黑背景 */
  display: flex;
  flex-direction: column;
  padding: 10px;
  /* 侧边栏独立滚动 */
  overflow-y: auto;
  border-right: 1px solid #e5e5e5;
}

.new-chat-btn {
  padding: 12px;
  border: 1px solid #e5e5e5;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 20px;
  font-size: 14px;
  text-align: left;
  transition: background 0.2s;
}
.new-chat-btn:hover {
  background-color: #e5e5e5;
}

.history-list {
  flex: 1; /* 占据剩余空间，把用户菜单挤下去 */
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.history-item {
  padding: 10px;
  font-size: 14px;
  color: #333;
  cursor: pointer;
  border-radius: 5px;
}
.history-item:hover {
  background-color: #e5e5e5;
}

.user-menu {
  padding: 10px;
  border-top: 1px solid #e5e5e5;
  margin-top: 10px;
  font-size: 14px;
  cursor: pointer;
}

/* --- 右侧主内容 --- */
.main-content {
  flex: 1; /* 占据剩余所有宽度 */
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: #ffffff;
}

.top-bar {
  padding: 10px 20px;
  font-weight: bold;
  /* 如果需要固定在顶部，可以使用 position: sticky */
}

/* 聊天内容区域：这是关键，必须独立滚动 */
.chat-container {
  flex: 1;
  overflow-y: auto; /* 只有这里滚动 */
  padding: 20px;
  scroll-behavior: smooth; /* 平滑滚动 */
}

/* 简单的输入框样式示例 */
.input-area {
  padding: 20px;
  border-top: 1px solid #f0f0f0;
}
.input-area input {
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  border: 1px solid #ccc;
}
</style>