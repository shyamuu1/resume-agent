from state import AgentState
from langgraph.graph import StateGraph, END
from nodes.cleaner import cleaner_node
from nodes.parser import parse_node
from nodes.analyzer import analyze_node
from nodes.rewriter import rewriter_node
from nodes.scorer import scorer_node
from utils.llm_utils import get_Logger

logger = get_Logger("StateGraphBuilder")

def should_retry(state: AgentState) -> str:
    logger.info(">>> Evaluating whether to retry based on ATS score and iteration count...")
    """
    Decision node — after scoring, decide whether to retry rewrite or finish.
    Retry conditions:
      - ATS score below 75
      - Haven't exceeded 3 attempts
    """
    ats_score = state.get("ats_score")
    iteration = state.get("iteration")

    if iteration >= 3:
        logger.info(f"   Exceeded maximum iterations. Finishing.")
        return END

    if ats_score < 75:
        logger.info(f"   Score {ats_score} below 75, retrying... (attempt {iteration + 1}/3)")
        return "rewriter"
    
    logger.info(f"   Score {ats_score} passed! Finishing.")
    return END

# Define the graph structure
def build_graph() -> StateGraph:
    builder = StateGraph(AgentState)
    logger.info("Building state graph with nodes: cleaner -> parser -> analyzer -> rewriter -> scorer")

    # Register nodes
    builder.add_node("cleaner", cleaner_node)
    builder.add_node("parser", parse_node)
    builder.add_node("analyzer", analyze_node)
    builder.add_node("rewriter", rewriter_node)
    builder.add_node("scorer", scorer_node)

    # Linear Edges 
    # cleaner -> parser -> analyzer -> rewriter -> scorer
    builder.set_entry_point("cleaner")
    builder.add_edge("cleaner", "parser")
    builder.add_edge("parser", "analyzer")
    builder.add_edge("analyzer", "rewriter")
    builder.add_edge("rewriter", "scorer")

    #Conditional retry loop
    builder.add_conditional_edges("scorer",
                                  should_retry,{
                                      "rewriter": "rewriter",
                                      END: END
                                  })
    return builder.compile()

graph = build_graph()