# Resume Tailoring Agent

A lightweight resume tailoring agent that scrapes a job posting, extracts keywords and requirements, analyzes resume fit, rewrites the resume to better match the job, and scores the result.

## Project Structure

- `resume_agent/main.py` — entrypoint for running the workflow.
- `resume_agent/graph.py` — defines the state graph and retry logic.
- `resume_agent/state.py` — typed agent state schema.
- `resume_agent/nodes/` — modular pipeline nodes:
  - `parser.py` — extracts keywords and requirements from the job description.
  - `analyzer.py` — compares resume content against requirements.
  - `rewriter.py` — rewrites the resume to improve relevance.
  - `scorer.py` — evaluates the tailored resume and generates suggestions.
- `resume_agent/tools/` — helper tools:
  - `scraper.py` — scrapes job posting text via Jina Reader.
  - `pdf_reader.py` — placeholder for PDF resume extraction.
- `resume_agent/test.py` — simple manual execution example.
- `resume_agent/output.txt` — sample output from a run.

## Requirements

This project depends on an LLM backend and a state graph library.

Suggested packages:

- `langchain_ollama`
- `langgraph`

Install them in your virtual environment:

```bash
python -m pip install langchain_ollama langgraph
```

> Note: If you use a different LLM provider or graph framework, update the node imports and initialization accordingly.

## Usage

Activate your Python environment, then run:

```bash
python resume_agent/main.py
```

The default `main.py` includes a sample job URL and resume snippet. To use a different job posting or resume, modify the `job_url` and `raw_resume` values in `resume_agent/main.py` or refactor the script to accept command-line arguments.

## Notes

- The pipeline currently expects the scraped job posting text to flow into the parser node via state. Ensure `main.py` populates the correct state field.
- `resume_agent/tools/pdf_reader.py` is currently a placeholder and does not implement PDF extraction.
- `resume_agent/test.py` is a simple script for local experimentation, not a formal test suite.

## Recommended Improvements

- Add a real dependency manifest such as `requirements.txt` or `pyproject.toml`.
- Implement stronger LLM response validation and error handling.
- Add unit tests using `pytest` or `unittest`.
- Replace direct `print()` debugging with structured logging.
