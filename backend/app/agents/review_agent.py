from __future__ import annotations

from typing import Any

from services.llm import invoke_json


def _heuristic_review(draft: str) -> dict[str, Any]:
    """
    在 LLM 审核链路不可用时，使用轻量规则进行审核。

    这里会故意采取保守策略：
    它只检查是否具备推动工作流继续前进的基本结构，
    而不是替代真正的人工投标审核。
    """

    text = draft.strip()
    missing_items = []

    if len(text) < 400:
        missing_items.append("Draft is too short.")

    has_technical = "Technical Proposal" in text or "技术方案" in text
    has_commercial = "Commercial Response" in text or "商务响应" in text
    has_plan = "Implementation Plan" in text or "实施计划" in text or "计划" in text

    if not has_technical:
        missing_items.append("Missing technical section.")
    if not has_commercial:
        missing_items.append("Missing commercial section.")
    if not has_plan:
        missing_items.append("Missing implementation plan details.")

    approved = not missing_items
    if approved:
        review = (
            "Automatic review passed. The draft includes the expected structure "
            "and can move to manual review."
        )
    else:
        review = "Automatic review failed: " + "; ".join(missing_items)

    return {"approved": approved, "review": review}


def review_agent(draft: str, bid_info: dict[str, Any] | None = None) -> dict[str, Any]:
    """
    审核生成后的草稿，并返回统一格式的决策结果。

    输出约定：
    - approved: bool
    - review: str
    """

    bid_info = bid_info or {}
    prompt = f"""
Review the following tender draft and return JSON:
{{
  "approved": true or false,
  "review": "feedback text"
}}

Focus on:
- overall structure completeness
- presence of technical and commercial sections
- implementation planning and service assurance
- alignment with the tender information

Tender info:
{bid_info}

Draft:
{draft}
""".strip()

    llm_result = invoke_json(
        prompt,
        system_prompt="You are a strict tender reviewer and return JSON only.",
    )
    if llm_result and "approved" in llm_result and "review" in llm_result:
        llm_result["approved"] = bool(llm_result["approved"])
        llm_result["review"] = str(llm_result["review"]).strip()
        return llm_result

    return _heuristic_review(draft)
