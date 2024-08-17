import json
import os

from anthropic import Anthropic
from dotenv import load_dotenv

from read_file import read_file
from write_to_file import write_to_file

load_dotenv(dotenv_path=".env")


# MODEL_NAME = "claude-3-opus-20240229"
MODEL_NAME = "claude-3-5-sonnet-20240620"


def create_anthropic_client() -> Anthropic:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = Anthropic(api_key=api_key)

    return client


client = create_anthropic_client()

PROMPT_TEMPLATE = """
Your task is to summarize and extract information from the paper in this JSON format: {output_format}.
# Requirements
1. The output should be a valid JSON file.
2. Make sure to include all authors

Here is paper content:<paper> {paper_content}</paper>
"""

OUTPUT_FORMAT_TEMPLATE = """
{
    "title": "title about the paper",
    "short_name": "a short name with snake case",
    "summary": "summary about the paper",
    "category": ["tag1", "tag2"],
    "authors": [
        {
            "name": "xxx",
            "affiliation": "xxx"
        }
    ],
    "publication_date": "xxx",
    "journal": "xxx",
    "doi": "xxx"
}
"""


def get_anthropic_completion(client, prompt) -> str:
    # https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb
    # https://github.com/anthropics/anthropic-cookbook/blob/main/misc/how_to_enable_json_mode.ipynb
    response = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2048,
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Here is the summary of the legal document: <json>"},
        ],
        stop_sequences=["</json>"],
    )

    return response.content[0].text


def process_paper(client, paper_path):
    print(f"Processing: {paper_path}")
    paper_content = read_file(paper_path)
    first_page_content = paper_content[:5000]
    prompt = PROMPT_TEMPLATE.format(output_format=OUTPUT_FORMAT_TEMPLATE, paper_content=first_page_content)
    print(f"Summarize: {paper_path}")
    summary_json_str = get_anthropic_completion(client, prompt)

    try:
        summary_json = json.loads(summary_json_str)
        short_name = summary_json.get("short_name", "unknown")
        output_path = f"{os.path.splitext(paper_path)[0]}_{short_name}.json"
        print(f"Write to file: output_path<{output_path}>, result: \n{summary_json_str}")
        write_to_file(file_path=output_path, content=summary_json_str.strip())
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for {paper_path}, summary_json_str:{summary_json_str}")


def main():
    paper_directory = "./papers/"
    paper_files = [f for f in os.listdir(paper_directory) if f.endswith(".pdf")]

    for paper_file in paper_files:
        paper_path = os.path.join(paper_directory, paper_file)
        process_paper(client, paper_path)


if __name__ == "__main__":
    # rye run python main_anthropic.py
    main()
