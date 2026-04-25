from __future__ import annotations

import re
from typing import Any

import fitz

from .llm import invoke_json


def parse_pdf(file_path: str) -> str:
    """
    读取 PDF 文件中的完整文本。

    这样可以保持解析逻辑简单稳定。
    如果后续扫描版 PDF 变多，可以在同一接口后面补充 OCR。
    """

    with fitz.open(file_path) as doc:
        return "\n".join(page.get_text() for page in doc)


def _clean_lines(text: str) -> list[str]:
    """将原始文档文本拆分为紧凑且非空的行。"""

    return [line.strip() for line in text.splitlines() if line.strip()]


def _match_after_keyword(lines: list[str], keywords: tuple[str, ...]) -> str:
    """
    提取出现在给定标签之后的值。

    这个辅助函数能处理的示例包括：
    - Project Name: XXX
    - Bid Deadline: 2026-05-01
    """

    for line in lines:
        compact_line = re.sub(r"\s+", " ", line)
        for keyword in keywords:
            pattern = rf"{re.escape(keyword)}[:：]?\s*(.+)"
            match = re.search(pattern, compact_line, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip()
    return ""


def _extract_technical_requirements(lines: list[str]) -> list[str]:
    """
    将看起来像需求项的行保留下来，作为轻量级本地提取回退方案。

    这不是完整的章节解析器。
    它刻意保持简单，以便在 LLM 不可用时后端仍能工作。
    """

    requirement_keywords = (
        "技术要求",
        "技术标准",
        "服务要求",
        "功能要求",
        "实施要求",
    )
    results: list[str] = []

    for line in lines:
        if any(keyword in line for keyword in requirement_keywords):
            results.append(line)

    return results[:8]


def _extract_bid_info_locally(text: str) -> dict[str, Any]:
    """在 LLM 链路不可用时，使用确定性规则提取招标信息。"""

    lines = _clean_lines(text)
    project_name = _match_after_keyword(
        lines,
        ("项目名称", "招标项目名称", "采购项目名称", "项目名", "Project Name"),
    )
    deadline = _match_after_keyword(
        lines,
        ("投标截止时间", "截止时间", "响应文件递交截止时间", "开标时间", "Deadline"),
    )
    requirements = _extract_technical_requirements(lines)

    return {
        "project_name": project_name or "Unknown project",
        "deadline": deadline or "Unknown deadline",
        "technical_requirements": requirements,
        "summary": "\n".join(lines[:10]),
    }


def extract_bid_info(text: str) -> dict[str, Any]:
    """
    从文档文本中提取关键招标字段。

    优先路径：
    1. 让 LLM 返回结构化 JSON
    2. 如果失败，再回退到确定性规则
    """

    prompt = f"""
Extract the key tender information from the document below and return JSON:
- project_name
- deadline
- technical_requirements
- summary

Document:
{text[:12000]}
""".strip()

    llm_result = invoke_json(
        prompt,
        system_prompt="You extract structured tender metadata and return only JSON.",
    )
    if llm_result:
        llm_result.setdefault("project_name", "Unknown project")
        llm_result.setdefault("deadline", "Unknown deadline")
        llm_result.setdefault("technical_requirements", [])
        llm_result.setdefault("summary", "")
        return llm_result

    return _extract_bid_info_locally(text)
