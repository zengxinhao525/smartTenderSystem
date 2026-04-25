from langgraph.graph import END, StateGraph

from .nodes import (
    generate_draft,
    human_review,
    parse_and_retrieve,
    review_draft,
    should_continue,
)
from .state import GraphState

# 将 should_continue 返回的路由标签映射到真实的图节点目标。
ROUTE_TO_NODE = {
    "rewrite": "write",
    "human": "human",
    "end": END,
    "force_end": END,
}


def build_graph():
    """
    构建招投标工作流图。

    执行路径：
    1. parse  -> 提取文本和结构化招标信息
    2. write  -> 生成技术标与商务标草稿
    3. review -> 决定重写、进入人工审核或结束
    4. human  -> 在最终完成前进入人工审核检查点
    """

    workflow = StateGraph(GraphState)

    workflow.add_node("parse", parse_and_retrieve)
    workflow.add_node("write", generate_draft)
    workflow.add_node("review", review_draft)
    workflow.add_node("human", human_review)

    workflow.set_entry_point("parse")

    workflow.add_edge("parse", "write")
    workflow.add_edge("write", "review")
    workflow.add_edge("human", END)

    # review 是控制枢纽，用于决定工作流接下来的分支。
    workflow.add_conditional_edges("review", should_continue, ROUTE_TO_NODE)

    return workflow.compile()
