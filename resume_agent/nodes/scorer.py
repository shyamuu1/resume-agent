# scorer.py
"""Scorer module."""
import json
import re
from state import AgentState
from langchain_ollama import OllamaLLM

llm = OllamaLLM(model="llama3.2")

def scorer_node(state:AgentState) -> dict:
    print(" >>> Running scorer node... ")
    
    prompt = f"""
     You are an ATS (Applicant Tracking System) and resume quality evaluator.

    Job Keywords:
    {json.dumps(state['jd_keywords'], indent=2)}

    Job Requirements:
    {json.dumps(state['jd_requirements'], indent=2)}

    Original Resume:
    {state['raw_resume']}

    Tailored Resume:
    {state['tailored_resume']}

    Evaluate the tailored resume on these criteria:

    1. KEYWORD MATCH: How many job keywords appear naturally in the tailored resume?
    2. REQUIREMENTS COVERAGE: How many job requirements are addressed?
    3. INTEGRITY CHECK: Does the tailored resume claim ANY skill, tool, or platform
       not present in the original resume? Flag each one explicitly.
    4. CLARITY: Are bullets concise and achievement-oriented?

    Respond ONLY with valid JSON, no explanation, no markdown:
    {{
        "ats_score": <integer 0-100>,
        "keyword_match_score": <integer 0-100>,
        "requirements_coverage_score": <integer 0-100>,
        "integrity_violations": ["list any fabricated or bridged skills here, empty if none"],
        "suggestions": ["specific actionable improvements"],
        "passed": <true if ats_score >= 75 and integrity_violations is empty, else false>
    }}
    """
    raw = llm.invoke(prompt)
    cleaned = re.sub(r"```json|```", "", raw).strip()

    try:
        parsed = json.loads(cleaned)
        ats_score = parsed.get("ats_score", 0)
        suggestions = parsed.get("suggestions", [])
        violations = parsed.get("integrity_violations", [])
        passed = parsed.get("passed", False)

    except:
        print("Warning: Could not parse scorer JSON")
        ats_score   = 0
        suggestions = []
        violations  = []
        passed      = False
    print(f"   ATS Score: {ats_score}/100 | Passed: {passed}")

    if violations:
        print(f"   ATS Score: {ats_score}/100 | Passed: {passed}")

    return {
        **state,
        "ats_score":   ats_score,
        "suggestions": suggestions
    }