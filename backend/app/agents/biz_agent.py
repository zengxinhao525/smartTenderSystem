from __future__ import annotations

from textwrap import dedent
from typing import Any

from app.services.llm import invoke_prompt


def _fallback_biz_response(context: str, bid_info: dict[str, Any]) -> str:
    """
    当 LLM 不可用时，返回一个确定性的商务响应内容。
    """

    return dedent(
        f"""
        # Commercial Response

        ## 1. Tender Basics
        Project Name: {bid_info.get("project_name", "Unknown project")}
        Deadline: {bid_info.get("deadline", "Unknown deadline")}

        ## 2. Commercial Commitments
        - We can align with the tender's delivery, acceptance, and support expectations.
        - We provide a stable execution team and clear collaboration structure.
        - We can support contract execution, milestone delivery, and post-delivery service.

        ## 3. Delivery Capability
        - Dedicated project staffing and cross-functional coordination.
        - Clear support and escalation process.
        - Ability to meet schedule and acceptance checkpoints.

        ## 4. Reference Context
        {context}
        """
    ).strip()


def biz_agent(context: str, bid_info: dict[str, Any] | None = None) -> str:
    """
    生成商务响应部分。

    这一部分强调商务承诺、服务能力和合同条款对齐，
    而不是技术实现细节。
    """

    bid_info = bid_info or {}
    # 生成商务响应部分
    prompt = f"""
Write the commercial response section for a tender proposal.

Requirements:
- cover commercial commitments, service capability, and clause alignment
- keep the tone formal and suitable for direct inclusion in a bid document
- avoid empty marketing language

Tender info:
{bid_info}

Additional context:
{context}
""".strip()

    response = invoke_prompt(
        prompt,
        system_prompt="You write formal and credible commercial tender responses.",
        temperature=0.2,
    )
    return response.strip() if response else _fallback_biz_response(context, bid_info)
