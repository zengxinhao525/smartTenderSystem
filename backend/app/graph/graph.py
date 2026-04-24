from langgraph.graph import StateGraph, END

from .state import GraphState
from .nodes import (
    parse_and_retrieve,
    generate_draft,
    review_draft,
    should_continue
)


def build_graph():
    workflow = StateGraph(GraphState)

    # 1️⃣ 注册节点
    workflow.add_node("parse", parse_and_retrieve)
    workflow.add_node("write", generate_draft)
    workflow.add_node("review", review_draft)
    workflow.add_node("human", human_review)

    # 2️⃣ 设置入口
    workflow.set_entry_point("parse")

    # 3️⃣ 流程连接
    workflow.add_edge("parse", "write")
    workflow.add_edge("write", "review")

    def should_continue(state: GraphState) -> str:
        if state["approved"]:
            return "human"

        if state["loop_count"] >= 3:
            return "end"

        return "rewrite"

    # 4️⃣ 条件分支（重点）
    workflow.add_conditional_edges(
        "review",
        should_continue,
        {
            "rewrite": "write",
            "human": "human",
            "end": END
        }
    )

    workflow.add_edge("human", END)