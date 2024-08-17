import json
import os

import openai
from dotenv import load_dotenv

from read_file import read_file
from write_to_file import write_to_file

load_dotenv(dotenv_path=".env")

MODEL_NAME = "gpt-4o-mini"
# MODEL_NAME = "gpt-4o"


def create_openai_client() -> openai.OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.OpenAI(api_key=api_key)
    return client


client = create_openai_client()

PROMPT_TEMPLATE = """
Your task is to summarize and extract information from the paper in this format: {output_format}.
The output should be a valid JSON file.
Here is paper content:{paper_content}
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


def get_openai_completion(client, paper_content) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": paper_content}],
        temperature=0,
        max_tokens=2000,  # Increase max tokens to accommodate longer responses
        # top_p=1,
        # frequency_penalty=0,
        # presence_penalty=0,
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


def process_paper(client, paper_path):
    print(f"Processing: {paper_path}")
    paper_content = read_file(paper_path)
    first_page_content = paper_content[:5000]
    prompt = PROMPT_TEMPLATE.format(output_format=OUTPUT_FORMAT_TEMPLATE, paper_content=first_page_content)
    print(f"Summarize: {paper_path}")
    summary_json_str = get_openai_completion(client, prompt)

    try:
        summary_json = json.loads(summary_json_str)
        short_name = summary_json.get("short_name", "unknown")
        output_path = f"{os.path.splitext(paper_path)[0]}_{short_name}.json"
        print(f"Write to file: output_path<{output_path}>, result: \n{summary_json_str}")
        write_to_file(file_path=output_path, content=summary_json_str)
    except json.JSONDecodeError:
        print(f"Failed to parse JSON for {paper_path}, summary_json_str:{summary_json_str}")


def main():
    paper_directory = "./papers/"
    paper_files = [f for f in os.listdir(paper_directory) if f.endswith(".pdf")]

    for paper_file in paper_files:
        paper_path = os.path.join(paper_directory, paper_file)
        process_paper(client, paper_path)


if __name__ == "__main__":
    main()
