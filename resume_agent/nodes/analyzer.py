# analyzer.py

import json
import re
from langchain_ollama import OllamaLLM
from state import AgentState


llm = OllamaLLM(model="llama3.2")

def analyze_node(state:AgentState) -> dict:
    print(">>> Running analyzer node ...")

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
    raw = llm.invoke(prompt)
    cleaned = re.sub(r"```json|```", "", raw).strip()
    try:
        parsed = json.loads(cleaned)
        gap_analysis = {
            "strong_matches": parsed.get("strong_matches", []),
            "weak_matches": parsed.get("weak_matches", []),
            "missing": parsed.get("missing", [])
        }
    except json.JSONDecodeError:
        print("Warning: Could not parse Json, defaulting to empty gap analysis.")
        gap_analysis = {
            "strong_matches": [],
            "weak_matches": [],
            "missing": []
        }
    strong = len(gap_analysis["strong_matches"])
    weak = len(gap_analysis["weak_matches"])
    missing = len(gap_analysis["missing"])
    print(f"Gap Analysis: {strong} strong matches, {weak} weak matches, {missing} missing requirements.")
    return {**state, "gap_analysis": gap_analysis}