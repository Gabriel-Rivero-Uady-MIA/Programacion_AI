"""Reuse the catalog analysis as a subgraph."""

from langgraph.graph import END, START, StateGraph
from workflow import (
    WorkflowState, normalize_topic, report_empty, route_documents,
    select_documents, summarize_documents,
)


def build_analysis_subgraph():
    builder = StateGraph(WorkflowState)
    builder.add_node("select", select_documents)
    builder.add_node("summarize", summarize_documents)
    builder.add_node("empty", report_empty)
    builder.add_edge(START, "select")
    builder.add_conditional_edges(
        "select", route_documents,
        {"found": "summarize", "empty": "empty"},
    )
    builder.add_edge("summarize", END)
    builder.add_edge("empty", END)
    return builder.compile()


def build_modular_workflow():
    analysis = build_analysis_subgraph()
    builder = StateGraph(WorkflowState)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("analysis", analysis)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "analysis")
    builder.add_edge("analysis", END)
    return builder.compile()
