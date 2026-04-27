from __future__ import annotations

from agents.biz_agent import biz_agent
from agents.review_agent import review_agent
from agents.tech_agent import tech_agent
from services.parser import extract_bid_info, parse_pdf
from services.retriever import retrieve_context

from .state import GraphState, merge_state


def parse_and_retrieve(state: GraphState) -> GraphState:
    """
    解析源 PDF，并为后续生成构建上下文。

    职责：
    - 从 file_path 读取文档
    - 提取结构化招标信息
    - 基于提取字段检索上下文知识
    """

    current_state = merge_state(state)
    file_path = current_state.get("file_path")

    if not file_path:
        raise ValueError("GraphState is missing file_path.")

    text = parse_pdf(file_path)
    bid_info = extract_bid_info(text)
    context = retrieve_context(bid_info)

    return {
        **current_state,
        "source_text": text,
        "bid_info": bid_info,
        "context": context,
        "messages": current_state["messages"]
        + [f"Parsed source file for project: {bid_info.get('project_name', 'unknown')}"],
    }


def generate_draft(state: GraphState) -> GraphState:
    """
    基于上下文和结构化招标信息生成投标草稿。

    草稿会明确分为两大部分：
    技术内容和商务响应。
    """

    current_state = merge_state(state)
    context = current_state.get("context", "")
    bid_info = current_state.get("bid_info", {})

    tech = tech_agent(context, bid_info=bid_info)
    biz = biz_agent(context, bid_info=bid_info)
    draft = f"{tech}\n\n{biz}".strip()

    return {
        **current_state,
        "draft": draft,
        "messages": current_state["messages"] + ["Generated a new tender draft."],
    }


def review_draft(state: GraphState) -> GraphState:
    """
    审核生成后的草稿，并更新流程控制标记。

    review      -> 面向人的审核反馈
    approved    -> 自动审核是否通过
    need_human  -> 工作流是否需要暂停等待人工审核
    """

    current_state = merge_state(state)
    result = review_agent(
        current_state.get("draft", ""),
        bid_info=current_state.get("bid_info", {}),
    )
    loop_count = current_state.get("loop_count", 0) + 1

    return {
        **current_state,
        "review": result["review"],
        "approved": result["approved"],
        "loop_count": loop_count,
        "need_human": result["approved"],
        "messages": current_state["messages"]
        + [f"Automatic review round {loop_count}: {'approved' if result['approved'] else 'rewrite'}."],
    }


def should_continue(state: GraphState) -> str:
    """
    决定 review 节点之后应进入哪个分支。

    规则：
    - 自动审核通过 -> 转入人工审核
    - 循环次数过多 -> 停止，避免无限重写
    - 其他情况     -> 继续重写并再次审核
    """

    current_state = merge_state(state)

    if current_state.get("approved"):
        return "human"

    if current_state.get("loop_count", 0) >= 3:
        return "force_end"

    return "rewrite"


def human_review(state: GraphState) -> GraphState:
    """
    人工审核检查点。

    该节点不会修改草稿。
    它只会将工作流标记为等待外部人工决策，之后再通过 /resume 回传。
    """

    current_state = merge_state(state)
    return {
        **current_state,
        "need_human": True,
        "messages": current_state["messages"] + ["Workflow paused for manual review."],
    }


def finalize_after_human_review(
    state: GraphState,
    approved: bool,
    review_notes: str | None = None,
) -> GraphState:
    """
    将人工审核结论写回工作流状态。

    状态会在这里更新，随后由路由处理器决定是结束流程，
    还是继续下一轮重写循环。
    """

    current_state = merge_state(state)
    review_text = review_notes or current_state.get("review", "")

    return {
        **current_state,
        "approved": approved,
        "need_human": False,
        "review": review_text,
        "messages": current_state["messages"]
        + [f"Manual review decision: {'approved' if approved else 'rejected'}."],
    }


def run_revision_cycle(state: GraphState) -> GraphState:
    """
    在不重新解析原始 PDF 的前提下继续执行写作/审核循环。

    这个函数主要用于 /resume 路由：
    当人工审核驳回后，或已有部分完成的状态已经具备足够上下文时，
    可以从这里继续推进流程。
    """

    current_state = merge_state(state)

    while True:
        route = should_continue(current_state)

        if route == "rewrite":
            current_state = generate_draft(current_state)
            current_state = review_draft(current_state)
            continue

        if route == "human":
            return human_review(current_state)

        current_state["need_human"] = False
        current_state["messages"] = current_state["messages"] + ["Workflow completed."]
        return current_state
