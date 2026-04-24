from docx import Document


def export_word(content: str, path="output.docx"):
    doc = Document()

    for line in content.split("\n"):
        doc.add_paragraph(line)

    doc.save(path)

    return path