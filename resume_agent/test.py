from nodes.parser import parse_node
from nodes.analyzer import analyze_node
from nodes.rewriter import rewriter_node
from nodes.scorer import scorer_node

state = {
    "job_description": """
        We are looking for a Senior Python Developer with experience in
        REST APIs, PostgreSQL, and AWS. The ideal candidate has 3+ years
        of backend development, strong communication skills, and experience
        with Docker and CI/CD pipelines.
    """,
    "raw_resume": """
        John Doe | john@email.com

        EXPERIENCE
        Backend Developer - Acme Corp (2 years)
        - Built REST APIs using Flask and FastAPI
        - Worked with MySQL databases
        - Deployed apps on Heroku

        SKILLS
        Python, Flask, FastAPI, MySQL, Git, Linux
    """,
    "jd_keywords": [],
    "jd_requirements": [],
    "gap_analysis": {},
    "tailored_resume": "",
    "ats_score": 0,
    "suggestions": [],
    "iteration": 0
}

# Chain all four nodes
state = parse_node(state)
state = analyze_node(state)
state = rewriter_node(state)
state = scorer_node(state)

print("\n--- Final Tailored Resume ---")
print(state["tailored_resume"])

print("\n--- Score Report ---")
print(f"  ATS Score:  {state['ats_score']}/100")
print(f"  Iteration:  {state['iteration']}")

print("\n--- Suggestions ---")
for s in state["suggestions"]:
    print(f"  • {s}")