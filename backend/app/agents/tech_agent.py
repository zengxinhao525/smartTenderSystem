# backend/app/agents/tech_agent.py

from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

llm = ChatOpenAI(
    temperature=0.3,
    model="gpt-4o-mini"  # 可替换成本地模型
)


def tech_agent(context: str) -> str:
    prompt = f"""
你是一名投标技术专家，请根据以下背景撰写“技术解决方案”：

{context}

要求：
- 结构清晰
- 专业严谨
- 分点说明
"""

    response = llm([HumanMessage(content=prompt)])
    return response.content