<template>
    <div class="container">
        <div class="left">
        <h3>日志</h3>
        <div v-for="log in logs" :key="log">{{ log }}</div>
        </div>

        <div class="right">
        <h3>标书内容</h3>
        <pre>{{ draft }}</pre>
        </div>
        <el-dialog v-model="showDialog">
            <pre>{{ draft }}</pre>

            <el-button @click="approve">通过</el-button>
            <el-button @click="reject">修改</el-button>
        </el-dialog>
    </div>
</template>

<script setup lang="ts">
    import { ref } from "vue";
    import { createSSE } from "@/api/sse";

    const logs = ref<string[]>([]);
    const draft = ref("");

    function start() {
    createSSE("http://localhost:8000/stream?file_path=test.pdf", (msg) => {
        logs.value.push(msg);

        if (msg.includes("write")) {
        draft.value += "\n" + msg;
        }
    });
    }

    function approve() {
        fetch("/resume", {
            method: "POST",
            body: JSON.stringify(currentState),
        });
    }
</script>