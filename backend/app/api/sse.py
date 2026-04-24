from sse_starlette.sse import EventSourceResponse
from app.graph.graph import build_graph

graph = build_graph()


async def stream_graph(state: dict):

    async def event_generator():
        for step in graph.stream(state):

            # step 是每个节点执行结果
            for node, value in step.items():

                yield {
                    "event": "message",
                    "data": f"[{node}] {value}"
                }

                # 🛑 如果进入人工节点 → 停止
                if node == "human":
                    yield {
                        "event": "pause",
                        "data": "等待人工审核"
                    }
                    return

    return EventSourceResponse(event_generator())