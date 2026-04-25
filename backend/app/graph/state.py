from __future__ import annotations

from typing import Any, TypedDict


class GraphState(TypedDict, total=False):
    """
    共享在 LangGraph 节点之间传递的状态。

    这将输入、中间产物和控制标志封装在一个对象中，
    以便每个节点都可以使用相同的合约。
    """

    file_path: str
    source_text: str
    bid_info: dict[str, Any]
    messages: list[str]
    context: str
    draft: str
    review: str
    loop_count: int
    approved: bool
    need_human: bool


def create_initial_state(file_path: str) -> GraphState:
    """
    为所有入口创建一致的初始状态。

    统一使用一个初始化函数，可以避免不同路由里重复维护默认字典。
    """

    return GraphState(
        file_path=file_path,
        source_text="",
        bid_info={},
        messages=[],
        context="",
        draft="",
        review="",
        loop_count=0,
        approved=False,
        need_human=False,
    )


def merge_state(state: dict[str, Any]) -> GraphState:
    """
    将外部传入的任意状态规范化为 GraphState。

    这样可以让 resume 相关处理逻辑兼容字段缺失或旧版本的载荷结构。
    """

    merged = create_initial_state(state.get("file_path", ""))
    merged.update(state)
    merged["messages"] = list(merged.get("messages", []))
    merged["bid_info"] = dict(merged.get("bid_info", {}))
    return merged
