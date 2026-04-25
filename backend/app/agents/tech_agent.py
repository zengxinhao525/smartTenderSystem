from __future__ import annotations

from textwrap import dedent
from typing import Any

from app.services.llm import invoke_prompt


def _fallback_tech_response(context: str, bid_info: dict[str, Any]) -> str:
    """
    在 LLM 链路不可用时，生成一个确定性的技术草稿。

    目标不是追求完美质量，
    而是保证在离线或环境配置不完整时，工作流仍然可用。
    """

    requirements = bid_info.get("technical_requirements") or [
        "Respond to the tender's technical requirements item by item."
    ]
    requirement_text = "\n".join(f"- {item}" for item in requirements)

    return dedent(
        f"""
        # Technical Proposal

        ## 1. Project Understanding
        Project Name: {bid_info.get("project_name", "Unknown project")}
        Deadline: {bid_info.get("deadline", "Unknown deadline")}
        This proposal is drafted from the tender document and the retrieved context.

        ## 2. Technical Response
        {requirement_text}

        ## 3. Implementation Plan
        - Organize the project into initiation, clarification, implementation, testing, and delivery phases.
        - Produce reviewable deliverables at each milestone.
        - Track project risks and maintain regular communication.

        ## 4. Service Assurance
        - Assign a project manager, technical lead, and delivery engineers.
        - Provide training, support, and post-delivery response mechanisms.

        ## 5. Reference Context
        {context}
        """
    ).strip()


def tech_agent(context: str, bid_info: dict[str, Any] | None = None) -> str:
    """
    生成投标响应中的技术部分。

    优先路径会使用 LLM 生成更丰富的内容；
    回退路径则返回结构化模板，确保下游节点始终能拿到可用结果。
    """

    bid_info = bid_info or {}
    prompt = f"""
Write the technical proposal section for a tender response.

Requirements:
- use clear subsection headings
- respond to technical requirements explicitly
- describe implementation approach, delivery plan, and service assurance
- keep the tone formal and production-ready

Tender info:
{bid_info}

Additional context:
{context}
""".strip()

    response = invoke_prompt(
        prompt,
        system_prompt="You write formal, professional tender technical proposals.",
        temperature=0.3,
    )
    return response.strip() if response else _fallback_tech_response(context, bid_info)
