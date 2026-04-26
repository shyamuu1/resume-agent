from graph import graph
from state import AgentState
from tools.scraper import scrape_job_description


def run_agent(job_url: str, raw_resume: str) -> AgentState:

    print("\n========================================")
    print("   Resume Tailoring Agent Starting...")
    print("========================================\n")

    print(">> Scraping job posting...")
    raw_job_posting = scrape_job_description(job_url)
    print(f"   Scraped {len(raw_job_posting)} characters")

    initial_state = {
        "raw_job_posting":        raw_job_posting,
        "raw_resume":             raw_resume,
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
    job_url = "https://job-boards.greenhouse.io/reddit/jobs/6909091?gh_src=8a8a4d8a1us"

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

    run_agent(job_url, raw_resume)