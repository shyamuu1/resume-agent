
import json
from state import AgentState
from utils import llm_utils

logger = llm_utils.get_Logger("AnalyzerNode")

def analyze_node(state:AgentState) -> dict:
    logger.info(">>> Running analyzer node ...")
    llm_utils.require_keys(state, "jd_requirements", "jd_keywords", "raw_resume")
    prompt = f"""
    Compare this resume against the job requirements and classify each requirement.

    Job Requirements:
    {json.dumps(state['jd_requirements'], indent=2)}

    Job Keywords:
    {json.dumps(state['jd_keywords'], indent=2)}

    Resume:
    {state['raw_resume']}

    Respond ONLY with valid JSON, no explanation, no markdown:
    {{
        "strong_matches": ["matched skill or requirement name, not resume text"],
        "weak_matches": ["requirement name and why it's a weak match"],
        "missing": ["requirement name not found in resume"]
    }}
    """

    cleaned = llm_utils.invoke_llm(prompt)
    try:
        parsed = llm_utils.parse_json(cleaned)
        gap_analysis = {
            "strong_matches": parsed.get("strong_matches", []),
            "weak_matches": parsed.get("weak_matches", []),
            "missing": parsed.get("missing", [])
        }
    except json.JSONDecodeError:
        logger.warning("Warning: Could not parse Json, defaulting to empty gap analysis.")
        gap_analysis = {
            "strong_matches": [],
            "weak_matches": [],
            "missing": []
        }
    strong = len(gap_analysis["strong_matches"])
    weak = len(gap_analysis["weak_matches"])
    missing = len(gap_analysis["missing"])
    logger.info(f"Gap Analysis: {strong} strong matches, {weak} weak matches, {missing} missing requirements.")
    return {**state, "gap_analysis": gap_analysis}