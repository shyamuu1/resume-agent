# parser.py
import json
import re
from langchain_ollama import OllamaLLM
from state import AgentState

#"""Parser module."""

# Get Model
llm = OllamaLLM(model="llama3.2")

example_output = {
    "keywords": ["Python", "REST APIs", "PostgreSQL", "AWS", "Docker", "Kubernetes", "CI/CD pipelines"],
    "requirements": ["5+ years of backend development", "strong communication skills"]
}


def parse_node(state: AgentState) -> AgentState:

    print(">>> Parsing Job Description and Resume...")
    # Prompt for parsing the job description and resume
    prompt = f""" 
    Analyze this job description and extract exact technology keywords and requirements.
    Job Description: {state['job_description']}
    Respond ONLY with valid JSON, no explanation, no markdown: {{ "keywords": [], requirements: []}}
    """
    # Invoke the LLM to get the raw response
    raw = llm.invoke(prompt)

    # Clean the response to extract the JSON part
    cleaned = re.sub(r"```json|```", "", raw).strip()

    # Parse the cleaned response to extract keywords and requirements
    # Handle potential JSON parsing errors gracefully by returning empty lists if parsing fails
    try:
        parsed = json.loads(cleaned)
        keywords = parsed.get("keywords", [])
        requirements = parsed.get("requirements", [])
    except json.JSONDecodeError:
        print("Warning: Failed to parse LLM response. Returning empty keywords and requirements.")
        keywords = []
        requirements = []
    
    print(f"found {len(keywords)} keywords, and requirements: {len(requirements)}")
    return {**state, "jd_keywords": keywords, "jd_requirements": requirements}


