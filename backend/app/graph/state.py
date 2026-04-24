from typing import List, TypedDict


class GraphState(TypedDict):
    messages: List[str]          # 对话历史
    context: str                 # 检索内容
    draft: str                   # 标书草稿
    review: str                  # 审核意见
    loop_count: int              # 循环计数
    approved: bool               # 是否通过审核
    need_human: bool             # 是否需要人工审核