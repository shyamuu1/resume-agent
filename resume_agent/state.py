from typing import TypedDict

class AgentState(TypedDict):
    #Inputs
    raw_job_posting: str
    
    raw_resume: str

    #Cleaned and structured
    job_description: str
    structured_job_posting: dict
    
    #Intermediate 
    jd_keywords: list[str]
    jd_requirements: list[str]
    gap_analysis: dict

    #Outputs
    tailored_resume: str
    ats_score:int
    suggestions: list[str]
    iteration: int