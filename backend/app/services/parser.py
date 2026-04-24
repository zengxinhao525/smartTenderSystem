import fitz  # PyMuPDF


def parse_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text

def extract_bid_info(text: str) -> dict:
    prompt = f"""
        从以下招标文件提取信息：

        {text}

        返回 JSON：
        - 项目名称
        - 截止时间
        - 技术要求
    """

    result = llm([HumanMessage(content=prompt)])

    return result.content."[END]"