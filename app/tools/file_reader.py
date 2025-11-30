import os
import pypdf
import docx
from google.adk.tools import ToolContext
from typing import Dict, List


def read_local_files(file_paths: str, tool_context: ToolContext) -> Dict:
    """
    Reads text from up to 3 local files (PDF, DOCX, TXT, MD, PY) located 
    under ./uploads directory.

    Always returns:
    {
        "success": bool,
        "files": [
            {
                "filename": str,
                "status": "ok" | "error",
                "content": str
            }
        ]
    }
    """
    
    os.makedirs(upload_dir, exist_ok=True)

    upload_dir = os.path.join(os.getcwd(), "uploads")

    paths = [p.strip().strip("'").strip('"') for p in file_paths.split(",")]

    if len(paths) > 3:
        return {
            "success": False,
            "message": "You can read up to 3 files only.",
            "files": []
        }

    results: List[Dict] = []

    for raw_path in paths:
        filename = os.path.basename(raw_path)
        path = os.path.join(upload_dir, filename)

        if not os.path.exists(path):
            results.append({
                "filename": filename,
                "status": "error",
                "content": f"File not found in uploads folder."
            })
            continue

        ext = os.path.splitext(path)[1].lower()

        try:
            if ext == ".pdf":
                reader = pypdf.PdfReader(path)
                text = "\n".join([page.extract_text() or "" for page in reader.pages])

            elif ext == ".docx":
                doc = docx.Document(path)
                text = "\n".join([para.text for para in doc.paragraphs])

            elif ext in [".txt", ".md", ".py"]:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()

            else:
                text = "[Unsupported file type]"

            results.append({
                "filename": filename,
                "status": "ok",
                "content": text
            })

        except Exception as e:
            results.append({
                "filename": filename,
                "status": "error",
                "content": f"Error reading file: {str(e)}"
            })

    # Final combined response
    return {
        "success": True,
        "files": results
    }
