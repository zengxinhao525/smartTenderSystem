from fastapi import Body, FastAPI

from api.routes import router
from graph.graph import build_graph
from graph.state import create_initial_state

app = FastAPI(
    title="智能招标系统后端",
    description="用于招标文件解析、起草、审查和导出的后端服务。",
)

# 在启动时只编译一次工作流，这样每次请求都可以复用
graph = build_graph()

app.include_router(router)


@app.get("/health")
def health() -> dict[str, str]:
    """用于前端或部署检查的简单健康检测接口"""

    return {"status": "ok"}


@app.post("/start")
def start(file_path: str = Body(..., embed=True)) -> dict:
    """
    从服务器上的文件路径启动完整工作流。

    当前后端假设 PDF 文件已经存在于磁盘上，
    只需要提供路径即可触发解析、起草和审查流程。
    """

    initial_state = create_initial_state(file_path)
    return graph.invoke(initial_state)