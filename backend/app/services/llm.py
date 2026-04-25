from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None

_ENV_LOADED = False


def _load_local_env() -> None:
    """按需加载 backend/.env，而不是在模块导入阶段立即加载。"""

    global _ENV_LOADED
    if _ENV_LOADED:
        return

    if load_dotenv is not None:
        env_path = Path(__file__).resolve().parents[2] / ".env"
        load_dotenv(env_path)

    _ENV_LOADED = True


def _build_chat_model(temperature: float):
    """
    延迟构建聊天模型。

    当模型或凭据不可用时，返回 None 而不是直接抛错，
    这样业务代码就可以回退到本地启发式逻辑。
    """

    _load_local_env()

    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from langchain_openai import ChatOpenAI
    except ImportError:  # pragma: no cover
        return None

    kwargs = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "temperature": temperature,
    }

    base_url = os.getenv("OPENAI_API_BASE")
    if base_url:
        kwargs["base_url"] = base_url

    return ChatOpenAI(**kwargs)


def invoke_prompt(
    prompt: str,
    *,
    system_prompt: str | None = None,
    temperature: float = 0.2,
) -> str | None:
    """调用 LLM 生成自由文本，并在失败时返回 None。"""

    model = _build_chat_model(temperature)
    if model is None:
        return None

    try:
        from langchain_core.messages import HumanMessage, SystemMessage
    except ImportError:  # pragma: no cover
        from langchain.schema import HumanMessage, SystemMessage

    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=prompt))

    try:
        response = model.invoke(messages)
    except Exception:
        return None

    return getattr(response, "content", None)


def _extract_json_block(text: str) -> dict[str, Any] | None:
    """
    从模型输出中提取 JSON 对象。

    很多模型会把 JSON 包在代码块里，
    这个辅助函数同时兼容纯 JSON 和 ```json 围栏内容。
    """

    if not text:
        return None

    candidate = text.strip()

    if "```" in candidate:
        parts = candidate.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("json"):
                part = part[4:].strip()
            try:
                return json.loads(part)
            except json.JSONDecodeError:
                continue

    try:
        return json.loads(candidate)
    except json.JSONDecodeError:
        return None


def invoke_json(
    prompt: str,
    *,
    system_prompt: str | None = None,
    temperature: float = 0.0,
) -> dict[str, Any] | None:
    """调用 LLM，并在可能时将回复解析为 JSON 对象。"""

    content = invoke_prompt(
        prompt,
        system_prompt=system_prompt,
        temperature=temperature,
    )
    parsed = _extract_json_block(content or "")
    if isinstance(parsed, dict):
        return parsed
    return None
