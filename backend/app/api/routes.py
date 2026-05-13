from fastapi import APIRouter, File, HTTPException, UploadFile

from api.schemas import ChatRequest, ChatResponse, UploadAnalysisResponse
from api.sse import stream_graph
from graph.graph import build_graph
from graph.nodes import finalize_after_human_review, run_revision_cycle
from graph.state import create_initial_state, merge_state
from services.chat import chat_with_history, resolve_chat_model_name
from services.exporter import export_word
from services.uploads import save_uploaded_pdf

router = APIRouter()

# 在这里保留一个已编译的图对象，方便路由处理器复用同一套工作流。
graph = build_graph()


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    """
    面向前端聊天页的直接问答接口。
    支持传入最近若干轮 history，后端会结合历史消息生成真实回复。
    """

    reply, fallback = chat_with_history(
        payload.message.strip(),
        payload.history,
    )
    return ChatResponse(
        reply=reply,
        model=resolve_chat_model_name(),
        fallback=fallback,
    )


@router.post("/upload", response_model=UploadAnalysisResponse)
async def upload_and_analyze(file: UploadFile = File(...)) -> UploadAnalysisResponse:
    """
    接收前端上传的 PDF，保存到本地后直接触发完整解析流程。
    """

    try:
        saved_path = await save_uploaded_pdf(file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    state = graph.invoke(create_initial_state(str(saved_path)))

    return UploadAnalysisResponse(
        file_name=file.filename or saved_path.name,
        file_path=str(saved_path),
        bid_info=state.get("bid_info", {}),
        draft=state.get("draft", ""),
        review=state.get("review", ""),
        approved=bool(state.get("approved", False)),
        need_human=bool(state.get("need_human", False)),
    )


@router.get("/stream")
async def start_stream(file_path: str):
    """
    通过 SSE 流式传输工作流执行事件。

    这对于需要按节点更新进度的 UI 很有帮助。
    """

    state = create_initial_state(file_path)
    return await stream_graph(state)


@router.post("/resume")
async def resume(state: dict):
    """
    继续已暂停或部分完成的工作流。

    当前行为以人工审核暂停点为中心：
    - 已批准的手动审核：直接返回最终化状态
    - 已拒绝的手动审核：继续重写/审核循环
    - 存在上下文但无暂停：继续本地修订流程
    - 仅存在 file_path：从头重新启动工作流
    """

    current_state = merge_state(state)

    if current_state.get("need_human"):
        human_approved = state.get("human_approved")
        human_review = state.get("human_review")

        if human_approved is None:
            raise HTTPException(
                status_code=400,
                detail="State is waiting for manual review. Provide human_approved.",
            )

        if human_approved:
            return finalize_after_human_review(
                current_state,
                approved=True,
                review_notes=human_review,
            )

        rejected_state = finalize_after_human_review(
            current_state,
            approved=False,
            review_notes=human_review or "Manual review rejected the draft.",
        )
        return run_revision_cycle(rejected_state)

    if current_state.get("context"):
        return run_revision_cycle(current_state)

    if current_state.get("file_path"):
        return graph.invoke(current_state)

    raise HTTPException(status_code=400, detail="Missing resumable state or file_path.")


@router.post("/export")
async def export_document(payload: dict):
    """
    将生成的文本导出到 Word 文档。

    接受的有效载荷键：
    - content: 要导出的原始文本
    - draft: 从工作流状态有效载荷直接导出当前草稿
    """

    content = payload.get("content") or payload.get("draft")
    if not content:
        raise HTTPException(status_code=400, detail="Missing content or draft.")

    output_path = export_word(content, payload.get("path"))
    return {"path": output_path}
