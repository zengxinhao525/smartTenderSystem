from __future__ import annotations

from pathlib import Path

from docx import Document


def export_word(content: str, path: str | None = None) -> str:
    """
    将生成的文本导出为 Word 文档。

    默认输出路径位于 backend/output.docx，
    这样后端生成的产物会保留在项目工作区内。
    """

    output_path = Path(path or "backend/output.docx")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = Document()
    for line in content.splitlines():
        doc.add_paragraph(line)

    doc.save(output_path)
    return str(output_path)
