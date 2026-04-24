from fastapi import APIRouter
from app.api.sse import stream_graph
from app.services.exporter import export_word

router = APIRouter()


@router.get("/stream")
async def start_stream(file_path: str):
    state = {
        "messages": [file_path],
        "context": "",
        "draft": "",
        "review": "",
        "loop_count": 0,
        "approved": False,
        "need_human": False
    }

    return await stream_graph(state)

@router.post("/resume")
async def resume(state: dict):

    result = graph.invoke(state)

    return result

