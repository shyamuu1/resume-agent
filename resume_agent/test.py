from nodes.parser import parse_node

test_state = {
    "job_description": """We are looking for a Senior Full-Stack Developer with experience in
    backend technologies like Spring REST APIs, Oracle, and AWS. Frontend technologies include React and Angular. 
    The ideal candidate has 3+ years of backend development,strong communication skills, strong problem-solving skills,
    and experience with Docker, Kubernetes and CI/CD pipelines.""",

    # default values for other fields

    "raw_resume": "",
    "jd_keywords": [],
    "jd_requirements": [],
    "gap_analysis": {},
    "tailored_resume": "",
    "ats_score": 0,
    "suggestions": [],
    "iteration": 0
}

example_output = {
    "jd_keywords": ["Python", "REST APIs", "PostgreSQL", "AWS", "Docker", "Kubernetes", "CI/CD pipelines"],
    "jd_requirements": ["5+ years of backend development", "strong communication skills"]
}

result = parse_node(test_state)

print("\n--- Keywords ---")
for kw in result["jd_keywords"]:
    print(f"- {kw}")

print("\n--- Requirements ---")
for req in result["jd_requirements"]:
    print(f"- {req}")

