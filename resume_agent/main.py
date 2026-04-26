from graph import graph
from state import AgentState

def run_agent(job_description: str, raw_resume: str) -> AgentState:
    print("\n========================================")
    print("   Resume Tailoring Agent Starting...")
    print("========================================\n")

    initial_state = {
        "job_description": job_description,
        "raw_resume":      raw_resume,
        "jd_keywords":     [],
        "jd_requirements": [],
        "gap_analysis":    {},
        "tailored_resume": "",
        "ats_score":       0,
        "suggestions":     [],
        "iteration":       0
    }

    result = graph.invoke(initial_state)

    print("\n========================================")
    print("   Agent Complete")
    print("========================================")
    print(f"\n Final ATS Score : {result['ats_score']}/100")
    print(f" Total Iterations: {result['iteration']}")

    print("\n--- Tailored Resume ---\n")
    print(result["tailored_resume"])

    print("\n--- Suggestions for Further Improvement ---")
    for s in result["suggestions"]:
        print(f"  • {s}")

    return result

if __name__ == "__main__":
    job_description = """
        We are looking for a Senior Python Developer with experience in
        REST APIs, PostgreSQL, and AWS. The ideal candidate has 3+ years
        of backend development, strong communication skills, and experience
        with Docker and CI/CD pipelines.
    """

    raw_resume = """
        John Doe | john@email.com

        EXPERIENCE
        Backend Developer - Acme Corp (2 years)
        - Built REST APIs using Flask and FastAPI
        - Worked with MySQL databases
        - Deployed apps on Heroku

        SKILLS
        Python, Flask, FastAPI, MySQL, Git, Linux
    """

    run_agent(job_description, raw_resume)