from typing import TypedDict

class AgentState(TypedDict):
    #Inputs
    job_description: str
    raw_resume: str

    #Intermediate 
    jd_keywords: list[str]
    jd_requirements: list[str]
    gap_analysis: dict

    #Outputs
    tailored_resume: str
    ats_score:int
    suggestions: list[str]
    iteration: int