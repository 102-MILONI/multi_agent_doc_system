import json
import PyPDF2

def detect_format(extension: str, content: str):
    ext = extension.lower()
    if ext == "pdf":
        return "PDF"
    elif ext == "json":
        return "JSON"
    elif ext in ["txt", "eml"]:
        return "Email"
    else:
        try:
            json.loads(content)
            return "JSON"
        except:
            return "Email"

def load_file(file_path: str) -> str:
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        try:
            reader = PyPDF2.PdfReader(file_path)
            text = "\n".join(page.extract_text() or "" for page in reader.pages)
            return text
        except Exception as e:
            raise RuntimeError(f"Error reading PDF: {e}")
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
