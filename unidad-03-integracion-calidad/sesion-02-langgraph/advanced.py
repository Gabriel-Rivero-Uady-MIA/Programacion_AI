"""Guided examples of parallel branches, reducers and Command."""

import asyncio
from operator import add
from typing import Annotated, Literal

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from pydantic import Field

from sample_data import DOCUMENTS
from workflow import (
    AnalysisResult, StateUpdate, WorkflowState, normalize_topic,
    report_empty, select_documents, summarize_documents,
)


async def count_documents(state: WorkflowState) -> StateUpdate:
    print("Count started")
    await asyncio.sleep(2)
    print("Count finished")
    return {"count": len(state.documents)}


async def count_pages(state: WorkflowState) -> StateUpdate:
    print("Pages started")
    await asyncio.sleep(2)
    print("Pages finished")
    return {"total_pages": sum(document["pages"] for document in state.documents)}


def format_summary(state: WorkflowState) -> StateUpdate:
    result = AnalysisResult(
        success=True, count=state.count, total_pages=state.total_pages
    )
    return {"message": f"Found {result.count} documents with {result.total_pages} pages."}


def build_parallel_workflow():
    builder = StateGraph(WorkflowState)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("select", select_documents)
    builder.add_node("count", count_documents)
    builder.add_node("pages", count_pages)
    builder.add_node("format", format_summary)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "select")
    builder.add_edge("select", "count")
    builder.add_edge("select", "pages")
    builder.add_edge(["count", "pages"], "format")
    builder.add_edge("format", END)
    return builder.compile()


class EventState(WorkflowState):
    events: Annotated[list[str], add] = Field(default_factory=list)


def record_count(state: EventState) -> StateUpdate:
    return {"events": [f"Count: {len(state.documents)}"]}


def record_pages(state: EventState) -> StateUpdate:
    total = sum(document["pages"] for document in state.documents)
    return {"events": [f"Pages: {total}"]}


def build_event_workflow():
    builder = StateGraph(EventState)
    builder.add_node("count", record_count)
    builder.add_node("pages", record_pages)
    builder.add_edge(START, "count")
    builder.add_edge(START, "pages")
    builder.add_edge("count", END)
    builder.add_edge("pages", END)
    return builder.compile()


def select_and_route(
    state: WorkflowState,
) -> Command[Literal["summarize", "empty"]]:
    selected = []
    for document in DOCUMENTS:
        if document["topic"] == state.topic:
            selected.append(document)
    destination = "summarize" if selected else "empty"
    return Command(update={"documents": selected}, goto=destination)


def build_command_workflow():
    builder = StateGraph(WorkflowState)
    builder.add_node("normalize", normalize_topic)
    builder.add_node("select", select_and_route)
    builder.add_node("summarize", summarize_documents)
    builder.add_node("empty", report_empty)
    builder.add_edge(START, "normalize")
    builder.add_edge("normalize", "select")
    builder.add_edge("summarize", END)
    builder.add_edge("empty", END)
    return builder.compile()
