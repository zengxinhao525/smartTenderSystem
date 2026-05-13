from __future__ import annotations

from api.schemas import ChatMessage
from services.llm import _build_chat_model, resolve_model_name

CHAT_SYSTEM_PROMPT = """
You are SmartTender AI, an assistant for tendering, bidding, proposal drafting, and document analysis.

Requirements:
- answer in Chinese unless the user clearly asks for another language
- be practical, structured, and concise
- if the question is unrelated to tendering, still answer helpfully
- avoid inventing unavailable project facts
""".strip()


def _fallback_chat_reply(message: str) -> str:
    return (
        "我已经收到你的问题：\n"
        f"{message}\n\n"
        "当前后端暂时没有拿到可用的大模型结果，所以先返回本地兜底回复。"
        "如果你希望我继续完善，可以检查模型配置，然后我再帮你把流式输出和更强的上下文能力也接上。"
    )


def chat_with_history(message: str, history: list[ChatMessage]) -> tuple[str, bool]:
    model = _build_chat_model(0.3)
    if model is None:
        return _fallback_chat_reply(message), True

    try:
        from langchain_core.messages import (
            AIMessage,
            HumanMessage,
            SystemMessage,
        )
    except ImportError:  # pragma: no cover
        from langchain.schema import AIMessage, HumanMessage, SystemMessage

    messages = [SystemMessage(content=CHAT_SYSTEM_PROMPT)]

    for item in history[-12:]:
        if item.role == "system":
            messages.append(SystemMessage(content=item.content))
        elif item.role == "assistant":
            messages.append(AIMessage(content=item.content))
        else:
            messages.append(HumanMessage(content=item.content))

    messages.append(HumanMessage(content=message))

    try:
        response = model.invoke(messages)
    except Exception:
        return _fallback_chat_reply(message), True

    content = getattr(response, "content", None)
    if not isinstance(content, str) or not content.strip():
        return _fallback_chat_reply(message), True

    return content.strip(), False


def resolve_chat_model_name() -> str:
    return resolve_model_name()
