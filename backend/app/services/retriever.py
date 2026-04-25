from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

_TEXT_CORPUS: list[str] = []
_VECTOR_DB = None
_VECTOR_DB_INITIALIZED = False


def _query_to_text(query: str | dict[str, Any]) -> str:
    """将字符串或结构化查询输入规范化为纯文本。"""

    if isinstance(query, str):
        return query

    return "\n".join(
        f"{key}: {value}"
        for key, value in query.items()
        if value not in ("", None, [], {})
    )


def _get_vector_db():
    """
    延迟初始化向量库。

    这样可以避免在缺少模型凭据或嵌入依赖未完整安装的环境里，
    在导入阶段就直接失败。
    """

    global _VECTOR_DB, _VECTOR_DB_INITIALIZED

    if _VECTOR_DB_INITIALIZED:
        return _VECTOR_DB

    _VECTOR_DB_INITIALIZED = True

    if not os.getenv("OPENAI_API_KEY"):
        return None

    try:
        from langchain_community.vectorstores import Chroma
    except ImportError:  # pragma: no cover
        try:
            from langchain.vectorstores import Chroma
        except ImportError:
            return None

    try:
        from langchain_openai import OpenAIEmbeddings
    except ImportError:  # pragma: no cover
        try:
            from langchain.embeddings import OpenAIEmbeddings
        except ImportError:
            return None

    persist_directory = Path(__file__).resolve().parents[2] / "chroma_db"
    persist_directory.mkdir(parents=True, exist_ok=True)

    try:
        _VECTOR_DB = Chroma(
            persist_directory=str(persist_directory),
            embedding_function=OpenAIEmbeddings(),
        )
    except Exception:
        _VECTOR_DB = None

    return _VECTOR_DB


def add_documents(texts: list[str]):
    """
    添加知识库文档。

    即使向量库不可用，文档也会先保存在内存中，
    这样检索仍然具备基本的本地回退能力。
    """

    documents = [text.strip() for text in texts if text and text.strip()]
    if not documents:
        return

    _TEXT_CORPUS.extend(documents)

    db = _get_vector_db()
    if db is None:
        return

    try:
        db.add_texts(documents)
    except Exception:
        return


def _keyword_score(query_text: str, document: str) -> int:
    """一个很轻量的关键词打分器，用于离线回退检索。"""

    tokens = {token for token in re.split(r"\W+", query_text.lower()) if token}
    document_lower = document.lower()
    return sum(1 for token in tokens if token in document_lower)


def retrieve_context(query: str | dict[str, Any], k: int = 3) -> str:
    """
    检索与当前招标任务相关的上下文信息。

    策略顺序：
    1. 优先使用向量检索
    2. 否则使用内存关键词检索
    3. 最后回退到结构化招标信息本身
    """

    query_text = _query_to_text(query)
    db = _get_vector_db()

    if db is not None:
        try:
            docs = db.similarity_search(query_text, k=k)
            if docs:
                return "\n\n".join(doc.page_content for doc in docs)
        except Exception:
            pass

    if _TEXT_CORPUS:
        ranked = sorted(
            _TEXT_CORPUS,
            key=lambda item: _keyword_score(query_text, item),
            reverse=True,
        )
        hits = [item for item in ranked[:k] if item]
        if hits:
            return "\n\n".join(hits)

    return f"No external knowledge base hit. Using structured tender info instead:\n{query_text}"
