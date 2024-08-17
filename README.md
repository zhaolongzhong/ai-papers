# AI Papers

A simple tool to summarize academic papers and extract key information in a structured format.

## Get Started

## Create .env file

```bash
cp .env.example .env
```

Update the API keys in the `.env` file

## Set up Rye
*Rye is a Python package and environment manager.*

[Install Rye](https://rye.astral.sh/guide/installation/)
```bash
curl -sSf https://rye.astral.sh/get | bash
```

Installs Dependencies:
```bash
rye sync
```

## Run
In `main.py`, set up `paper_directory`, then run,

```bash
./run.sh
```
or 
```bash
rye run python main.py
```

## Resources
- [Summarization with Claude](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb)
- [Long Document Content Extraction](https://github.com/openai/openai-cookbook/blob/main/examples/Entity_extraction_for_long_documents.ipynb)
- [How to evaluate a summarization task](https://github.com/openai/openai-cookbook/blob/main/examples/evaluation/How_to_eval_abstractive_summarization.ipynb)
- [Question answering using embeddings-based search](https://github.com/openai/openai-cookbook/blob/main/examples/Question_answering_using_embeddings.ipynb)
- [Embedding Wikipedia articles for search](https://github.com/openai/openai-cookbook/blob/main/examples/Embedding_Wikipedia_articles_for_search.ipynb)