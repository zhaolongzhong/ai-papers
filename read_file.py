import os

from pypdf import PdfReader


def read_file(file_path: str, encoding: str = "utf-8") -> str:
    """Read a file (text or PDF) and return its contents as a string."""
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."

    try:
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            text = "".join(page.extract_text() for page in reader.pages)
            return text
        else:
            with open(file_path, encoding=encoding) as f:
                return f.read()
    except Exception as error:
        return f"Error: {error}"
