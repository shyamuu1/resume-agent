
import json
from utils import llm_utils
from state import AgentState


example_output = {
    "keywords": ["Python", "REST APIs", "PostgreSQL", "AWS", "Docker", "Kubernetes", "CI/CD pipelines"],
    "requirements": ["5+ years of backend development", "strong communication skills"]
}


logger = llm_utils.get_Logger("ParserNode")

def parse_node(state: AgentState) -> AgentState:

    logger.info(">>> Parsing Job Description and Resume...")
    llm_utils.require_keys(state, "job_description")
    # Prompt for parsing the job description and resume
    prompt = f""" 
    Analyze this job description and extract exact technology keywords and requirements.
    Job Description: {state['job_description']}
    Respond ONLY with valid JSON, no explanation, no markdown: {{ "keywords": [], requirements: []}}
    """
    # Invoke the LLM to get the raw response
    cleaned = llm_utils.invoke_llm(prompt)

    # Parse the cleaned response to extract keywords and requirements
    # Handle potential JSON parsing errors gracefully by returning empty lists if parsing fails
    try:
        parsed = llm_utils.parse_json(cleaned)
        keywords = parsed.get("keywords", [])
        requirements = parsed.get("requirements", [])
    except json.JSONDecodeError:
        logger.warning("Warning: Failed to parse LLM response. Returning empty keywords and requirements.")
        keywords = []
        requirements = []
    
    logger.info(f"found {len(keywords)} keywords, and requirements: {len(requirements)}")
    return {**state, "jd_keywords": keywords, "jd_requirements": requirements}


