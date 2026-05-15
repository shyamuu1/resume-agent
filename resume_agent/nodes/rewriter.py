# rewriter.py
"""Rewriter module."""

import json
from state import AgentState
from utils.llm_utils import get_Logger, invoke_llm, require_keys


logger = get_Logger("RewriterNode")

def rewriter_node(state: AgentState) -> dict:
    logger.info(">>> Running rewriter node ...")
    require_keys(state, "jd_keywords", "gap_analysis", "raw_resume", "iteration")
    gap = state["gap_analysis"]
    prompt = f"""
    You are a professional resume writer. Rewrite the resume below to better match the job.

    Job Keywords to naturally include:
    {json.dumps(state['jd_keywords'], indent=2)}

    Gap Analysis:
    - Strong (keep and emphasize): {json.dumps(gap['strong_matches'], indent=2)}
    - Weak (rewrite to strengthen): {json.dumps(gap['weak_matches'], indent=2)}
    - Missing (add context if any related experience exists): {json.dumps(gap['missing'], indent=2)}

    Original Resume:
    {state['raw_resume']}
    
    Rules you MUST follow:
    1. Do NOT invent jobs, degrees, or experience that isn't in the original resume
    2. DO rephrase bullets to use keywords from the job description naturally
    3. DO reorder bullets to lead with most relevant experience
    4. DO strengthen weak matches with more specific language
    5. For missing skills:
       - ONLY mention a skill if it explicitly exists in the original resume
       - NEVER treat different cloud platforms as equivalent (Heroku ≠ AWS, GCP, Azure)
       - NEVER treat different databases as equivalent (MySQL ≠ PostgreSQL, MongoDB ≠ DynamoDB)
       - If a skill is truly missing, leave it out entirely — do not bridge or imply it
    6. Keep the same overall structure (header, experience, skills)
    7. Output ONLY the rewritten resume text, no explanation

    Rewritten Resume:
    """
    tailored = invoke_llm(prompt)
    logger.info(f"   Rewrite Complete - {len(tailored)-1} words")
    return {**state, "tailored_resume": tailored, "iteration": state["iteration"] + 1}