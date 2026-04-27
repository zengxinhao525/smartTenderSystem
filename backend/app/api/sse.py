import json

from sse_starlette.sse import EventSourceResponse

from graph.graph import build_graph

# SSE 使用与常规 API 路由相同的工作流定义。
graph = build_graph()


async def stream_graph(state: dict):
    """
    将 LangGraph 的步骤输出转换为 SSE 事件。

    每个流式步骤的形状为 {node_name: state}，
    这样前端就可以按节点名称渲染执行进度。
    """

    async def event_generator():
        for step in graph.stream(state):
            for node, value in step.items():
                yield {
                    "event": "message",
                    "data": json.dumps(
                        {"node": node, "state": value},
                        ensure_ascii=False,
                    ),
                }

                # 当工作流到达人审节点时，暂停流式传输。
                if node == "human":
                    yield {
                        "event": "pause",
                        "data": json.dumps(
                            {"message": "Waiting for manual review", "state": value},
                            ensure_ascii=False,
                        ),
                    }
                    return

        yield {
            "event": "end",
            "data": json.dumps({"message": "Workflow completed"}, ensure_ascii=False),
        }

    return EventSourceResponse(event_generator())
