import logging
import re
import json
from langchain_ollama import OllamaLLM
from typing import List, Dict, Any

from resume_agent.exception import AgentError, AgentErrorCode

_llm: OllamaLLM | None = None

def get_llm() -> OllamaLLM:
    global _llm
    if _llm is None:
        _llm =OllamaLLM(model="llama3.2")
    return _llm

def get_Logger(name:str) -> logging.Logger:
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)

def clean_llm_output(raw: str) -> str:
   logging.info("Cleaning LLM output...")
   return re.sub(r"```json|```", "", raw).strip()

def invoke_llm(prompt:str) -> str:
    llm = get_llm()
    try:
        raw_response = llm.invoke(prompt)
        return clean_llm_output(raw_response)
    except Exception as ex:
        logging.warning(f"LLM invocation failed: {ex}")
        raise AgentError(AgentErrorCode.LLM_INVOCATION_ERROR, "Failed to invoke LLM", details=str(ex))

def parse_json(raw: str) -> dict:
    try:
        return json.loads(raw)
    except json.JSONDecodeError as ex:
        logging.warning(f"Failed to parse JSON: {ex}")
        raise AgentError(AgentErrorCode.JSON_PARSING_ERROR, "Failed to parse JSON from LLM response", details=str(ex))

def require_keys(state:dict, *keys):
    missing = [key for key in keys if key not in state]
    if missing:
        raise AgentError(AgentErrorCode.STATE_VALIDATION_ERROR, f"Missing required keys in state: {missing}")
    
