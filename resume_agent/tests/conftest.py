import json

import pytest

@pytest.fixture
def sample_state() -> dict:
    return {
        "raw_job_posting":        mock_job_posting(),
        "raw_resume":             mock_resume(),
        "job_description":        "",
        "structured_job_posting": {},
        "jd_keywords":            [],
        "jd_requirements":        [],
        "gap_analysis":           {},
        "tailored_resume":        "",
        "ats_score":              0,
        "suggestions":            [],
        "iteration":              0
    }

@pytest.fixture
def mock_invoke_llm(monkeypatch):
    def mock_invoke(prompt: str) -> str:
        if "Extract only the relevant job information" in prompt:
            return json.dumps({
                "job_title": "Backend Developer",
                "company": "Acme Corp",
                "location": "Remote",
                "remote_policy": "Remote",
                "salary": "$80k-$100k",
                "description": "Develop and maintain REST APIs using Python frameworks.",
                "required_qualifications": ["2+ years of experience in backend development", "Proficiency in Python and web frameworks"],
                "nice_to_haves": ["Experience with SQL databases", "Familiarity with cloud deployment"],
                "about_company": "Acme Corp is a leading tech company specializing in innovative solutions."
            })
        elif "Analyze this job description and extract exact technology keywords and requirements" in prompt:
            return json.dumps({
                "keywords": ["Python", "Flask", "FastAPI", "MySQL", "AWS"],
                "requirements": ["2+ years of experience in backend development", "Proficiency in Python and web frameworks", "Experience with SQL databases", "Familiarity with cloud deployment"]
            })
        elif "Compare this resume against the job requirements and classify each requirement" in prompt:
            return json.dumps({
                "strong_matches": ["2+ years of experience in backend development", "Proficiency in Python and web frameworks"],
                "weak_matches": ["Experience with SQL databases (worked with MySQL, but not PostgreSQL)", "Familiarity with cloud deployment (deployed on Heroku, but no direct AWS experience)"],
                "missing": []
            })
        else:
            return "{}"
    
    monkeypatch.setattr("resume_agent.utils.llm_utils.invoke_llm", mock_invoke)

def mock_resume() -> str:
    return """
        John Doe | john@email.com

        EXPERIENCE
        Backend Developer - Acme Corp (2 years)
        - Built REST APIs using Flask and FastAPI
        - Worked with MySQL databases
        - Deployed apps on Heroku

        SKILLS
        Python, Flask, FastAPI, MySQL, Git, Linux
    """

def mock_job_posting() -> str:
    return """
    Job Title: Backend Developer

    Responsibilities:
    - Develop and maintain REST APIs using Python frameworks (Flask, FastAPI)
    - Work with relational databases (PostgreSQL, MySQL)
    - Deploy and manage applications on cloud platforms (AWS, GCP, Azure)

    Requirements:
    - 2+ years of experience in backend development
    - Proficiency in Python and web frameworks
    - Experience with SQL databases
    - Familiarity with cloud deployment
    """

