import re
import json
from state import AgentState
from utils import llm_utils

#Patterns to strip before using LLM
NOISE_PATTERNS = [
    r"Posted \d+ days? ago",
    r"\d+ applicants?",
    r"Share\s*Save\s*Apply",
    r"Subscribe to Premium.*",
    r"Similar jobs.*",
    r"Privacy Policy.*",
    r"Terms of Service.*",
    r"Footer.*",
    r"\[Advertisement\]",
    r"http\S+",              # stray URLs
    r"#{1,6}\s*",            # markdown headers from Jina
]

logger = llm_utils.get_Logger("CleanerNode")

def clean_raw_text(text:str) -> str:
    for pattern in NOISE_PATTERNS:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE)
    
    #Collapse multiple blank lines and trim
    text = re.sub(r"\n{3,}","\n\n",text)
    return text.strip()

def cleaner_node(state: AgentState) -> dict:
    logger.info(">>> Cleaning raw job description and resume text...")
    llm_utils.require_keys(state, "job_description")
    #1. Clean noise patterns
    pre_cleaned = clean_raw_text(state["job_description"])

    #2 LLM based structuring
    prompt = f"""
    You are a data cleaning assistant. Extract only the relevant job
    information from this text and return it as structured JSON.

    Remove all of the following:
    - Navigation elements, buttons, links
    - Advertisements or promotional content
    - Recommended jobs or similar listings
    - Footer, privacy policy, terms of service
    - Any metadata like view counts or application counts

    Keep only:
    - Job title
    - Company name
    - Location and remote policy
    - Salary if mentioned
    - Job description
    - Required qualifications
    - Nice to have qualifications
    - About the company (if present)

    Raw text:
    {pre_cleaned}

    Respond ONLY with valid JSON, no explanation, no markdown:
    {{
        "job_title": "",
        "company": "",
        "location": "",
        "remote_policy": "",
        "salary": "",
        "description": "",
        "required_qualifications": [],
        "nice_to_haves": [],
        "about_company": ""
    }}
    """
    cleaned = llm_utils.invoke_llm(prompt)

    try:
        structured = llm_utils.parse_json(cleaned)
        #Rebuild a clean job description for down stream nodes
        cleaned_jd = f"""
        Job Title: {structured.get('job_title', '')}
        Company: {structured.get('company', '')}
        Location: {structured.get('location', '')}
        Salary: {structured.get('salary', '')}

        About the role:
        {structured.get('description', '')}

        Required Qualifications:
        {chr(10).join(f"- {qualification}" for qualification in structured.get('required_qualifications', []))}

        Nice to Haves:
        {chr(10).join(f"- {qualification}" for qualification in structured.get('nice_to_haves', []))}

        About the Company:
        {structured.get('about_company', '')}
        """

        logger.info(f"   Cleaned: {structured.get('job_title')} at {structured.get('company')}")
    except json.JSONDecodeError:
        logger.warning("   Warning: Could not structure JSON, using pre-cleaned text")
        cleaned_jd = pre_cleaned
        structured = {}
        
    return {**state, "job_description": cleaned_jd, "structured_job_posting": structured}