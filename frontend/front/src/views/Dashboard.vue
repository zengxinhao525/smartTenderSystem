<template>
    <div>
        <h2>项目看板</h2>

        <el-table :data="projects">
        <el-table-column prop="name" label="项目名称" />
        <el-table-column prop="status" label="状态" />
        </el-table>
    </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const projects = ref([
  { name: "智慧城市项目", status: "解析中" },
  { name: "AI平台投标", status: "撰写中" },
]);
</script>