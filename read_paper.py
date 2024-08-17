import json
import os

from pypdf import PdfReader


def read_first_page_of_pdf(file_path: str) -> str:
    """Read the first page of a PDF file and return its contents as a string."""
    if not os.path.isfile(file_path):
        return f"Error: The file {file_path} does not exist."

    try:
        if file_path.lower().endswith(".pdf"):
            reader = PdfReader(file_path)
            if reader.pages:
                return reader.pages[0].extract_text()
            else:
                return "Error: No pages found in PDF."
        else:
            return f"Error: {file_path} is not a PDF file."
    except Exception as error:
        return f"Error: {error}"


def process_papers_in_folder(folder_path: str, output_folder: str) -> None:
    """Process all PDF files in a folder, read the first page, and write to a JSON file."""
    if not os.path.isdir(folder_path):
        print(f"Error: The folder {folder_path} does not exist.")
        return

    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(".pdf"):
            file_path = os.path.join(folder_path, file_name)
            text = read_first_page_of_pdf(file_path)

            # Create the output JSON file path
            output_file_name = f"{os.path.splitext(file_name)[0]}.json"
            output_file_path = os.path.join(output_folder, output_file_name)

            # Write the text to the JSON file
            with open(output_file_path, "w", encoding="utf-8") as json_file:
                json.dump({"first_page_text": text}, json_file, ensure_ascii=False, indent=4)

            print(f"Processed and saved: {output_file_path}")


# Example usage:
folder_path = "./papers"
output_folder = "./papers/output_json"
process_papers_in_folder(folder_path, output_folder)

# rye run python read_paper.py
