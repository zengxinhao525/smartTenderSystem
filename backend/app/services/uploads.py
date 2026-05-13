from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile

UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


def _sanitize_filename(file_name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", file_name).strip("._")
    return cleaned or "upload.pdf"


async def save_uploaded_pdf(file: UploadFile) -> Path:
    if not file.filename:
        raise ValueError("Missing file name.")

    suffix = Path(file.filename).suffix.lower()
    if suffix != ".pdf":
        raise ValueError("Only PDF files are supported.")

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    safe_name = _sanitize_filename(file.filename)
    output_path = UPLOAD_DIR / f"{timestamp}_{safe_name}"

    content = await file.read()
    output_path.write_bytes(content)
    return output_path
