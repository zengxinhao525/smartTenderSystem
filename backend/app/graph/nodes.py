from .state import GraphState
from app.services.parser import parse_pdf, extract_bid_info
from app.services.retriever import retrieve_context
from app.agents.tech_agent import tech_agent
from app.agents.biz_agent import biz_agent
from app.agents.review_agent import review_agent


from app.services.parser import parse_pdf, extract_bid_info

def parse_and_retrieve(state: GraphState) -> GraphState:
    file_path = state["messages"][0]

    text = parse_pdf(file_path)

    # ⭐ 新增
    structured = extract_bid_info(text)

    context = retrieve_context(structured)

    return {
        **state,
        "context": context,
        "messages": state["messages"] + [structured]
    }

def generate_draft(state: GraphState) -> GraphState:
    print("✍️ 多智能体写作中...")

    context = state["context"]

    tech = tech_agent(context)
    biz = biz_agent(context)

    draft = tech + "\n\n" + biz

    return {
        **state,
        "draft": draft,
    }

def review_draft(state: GraphState) -> GraphState:
    print("🧠 审核智能体检查中...")

    result = review_agent(state["draft"])

    loop_count = state["loop_count"] + 1

    return {
        **state,
        "review": result["review"],
        "approved": result["approved"],
        "loop_count": loop_count,
        "need_human": result["approved"]  # 通过才进入人工
    }

def should_continue(state: GraphState) -> str:
    if state["approved"]:
        return "end"

    if state["loop_count"] >= 3:
        return "force_end"

    return "rewrite"

def human_review(state: GraphState) -> GraphState:
    print("🛑 等待人工审核...")

    # ⚠️ 这里不做任何处理，等待外部输入
    return state