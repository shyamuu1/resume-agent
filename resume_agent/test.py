from nodes.parser import parse_node
from nodes.analyzer import analyze_node

# Run parser first, feed output into analyzer
test_state = {
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

# Chain the two nodes
test_state = parse_node(test_state)
test_state = analyze_node(test_state)

print("\n--- Gap Analysis ---")
print("\n Strong Matches:")
for item in test_state["gap_analysis"]["strong_matches"]:
    print(f"   ✓ {item}")

print("\n Weak Matches:")
for item in test_state["gap_analysis"]["weak_matches"]:
    print(f"   ~ {item}")

print("\n Missing:")
for item in test_state["gap_analysis"]["missing"]:
    print(f"   ✗ {item}")

