def review_agent(draft: str) -> dict:
    prompt = f"""
        请检查以下标书是否合规：

        {draft}

        只返回：
        通过 或 不通过，并说明原因
    """