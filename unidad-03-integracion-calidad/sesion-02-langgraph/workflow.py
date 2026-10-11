"""Analyze a document catalog with a Pydantic graph state."""

from typing import Literal

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, ConfigDict, Field

from sample_data import DOCUMENTS, Document

StateUpdate = dict[str, object]


class WorkflowState(BaseModel):
    topic: str
    original_topic: str = ""
    documents: list[Document] = Field(default_factory=list)
    count: int = 0
    total_pages: int = 0
    message: str = ""


class AnalysisResult(BaseModel):
    model_config = ConfigDict(strict=True)

    success: bool
    error: str = ""
    count: int = Field(ge=0)
    total_pages: int = Field(ge=0)


def normalize_topic(state: WorkflowState) -> StateUpdate:
    topic = state.topic.strip().lower()
    if not topic:
        raise ValueError("topic must not be blank")
    return {"original_topic": state.topic, "topic": topic}


def select_documents(state: WorkflowState) -> StateUpdate:
    selected = []
    for document in DOCUMENTS:
        if document["topic"] == state.topic:
            selected.append(document)
    return {"documents": selected}


def route_documents(state: WorkflowState) -> Literal["found", "empty"]:
    if state.documents:
        return "found"
    return "empty"


def summarize_documents(state: WorkflowState) -> StateUpdate:
    raw_result = {
        "success": True,
        "count": len(state.documents),
        "total_pages": sum(document["pages"] for document in state.documents),
    }
    result = AnalysisResult.model_validate(raw_result)
    return {
        "count": result.count,
        "total_pages": result.total_pages,
        "message": f"Found {result.count} documents with {result.total_pages} pages.",
    }


def report_empty(state: WorkflowState) -> StateUpdate:
    return {
        "count": 0,
        "total_pages": 0,
        "message": f"No documents found for topic: {state.topic}",
    }


def build_workflow():
    builder = StateGraph(WorkflowState)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("select", select_documents)
    builder.add_node("summarize", summarize_documents)
    builder.add_node("empty", report_empty)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "select")
    builder.add_conditional_edges(
        "select", route_documents,
        {"found": "summarize", "empty": "empty"},
    )
    builder.add_edge("summarize", END)
    builder.add_edge("empty", END)
    return builder.compile()
