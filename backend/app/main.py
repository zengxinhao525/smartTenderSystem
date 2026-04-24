from fastapi import FastAPI
from app.graph.graph import build_graph
from app.api.routes import router

app = FastAPI()

graph = build_graph()

app.include_router(router)


@app.post("/start")
def start(file_path: str):
    state = {
        "messages": [file_path],
        "context": "",
        "draft": "",
        "review": "",
        "loop_count": 0,
        "approved": False,
        "need_human": False
    }

    result = graph.invoke(state)

    return result