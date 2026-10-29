from datetime import datetime, timezone
import json
from pathlib import Path

from sparql.queries import (
    build_load_decision_documents_query,
    build_load_task_input_files_query,
    build_load_task_query,
    build_update_decision_document_html_query,
    build_update_task_status_query,
    build_load_job_of_task_query,
)
from sparql.client import query, update
from utils.utils import physical_uri_to_path

class TaskNotFoundError(Exception):
    pass

class TaskInputNotFoundError(Exception):
    pass

class DecisionDocumentNotFoundError(Exception):
    pass

class JobNotFoundError(Exception):
    pass

def load_task(task_uri):
    results = query(build_load_task_query(task_uri))
    bindings = results["results"]["bindings"]

    if not bindings:
        raise TaskNotFoundError(
            f"Task not found: {task_uri}"
        )

    if len(bindings) > 1:
        graphs = [
            item["graph"]["value"]
            for item in bindings
        ]

        raise RuntimeError(
            f"Task {task_uri} was found multiple times in graphs: "
            f"{graphs}"
        )

    item = bindings[0]

    return {
        "uri": task_uri,
        "graph": item["graph"]["value"],
        "status": item["status"]["value"],
        "operation": item["operation"]["value"],
    }


def load_job_uri_of_task(task_uri, graph):
    results = query(build_load_job_of_task_query(task_uri, graph))
    bindings = results["results"]["bindings"]

    if not bindings:
        raise JobNotFoundError(f"No job found for task: {task_uri}")

    if len(bindings) > 1:
        raise RuntimeError(f"Task {task_uri} belongs to multiple jobs")

    return bindings[0]["job"]["value"]


def load_task_input_files(task_uri, graph):
    results = query(build_load_task_input_files_query(task_uri, graph))
    bindings = results["results"]["bindings"]

    if not bindings:
        raise TaskInputNotFoundError(
            f"No input files found for task: {task_uri}"
        )

    files = []

    for item in bindings:
        filename = item["filename"]["value"]

        physical_file_uri = item["physicalFile"]["value"]
        source_path = physical_uri_to_path(physical_file_uri)

        files.append({
            "container_uri": item["container"]["value"],
            "logical_file_uri": item["logicalFile"]["value"],
            "physical_file_uri": item["physicalFile"]["value"],
            "filename": filename,
            "source_path": source_path,
            "mime_type": item.get("format", {}).get("value"),
        })

    return files


def load_decision_documents_for_file(logical_file_uri, graph):
    results = query(
        build_load_decision_documents_query(logical_file_uri, graph)
    )
    documents = [
        item["decisionDocument"]["value"]
        for item in results["results"]["bindings"]
    ]

    if not documents:
        raise DecisionDocumentNotFoundError(
            "No decision document is linked to input file: "
            f"{logical_file_uri}"
        )

    return documents


def update_decision_document_html(
    decision_document_uri,
    logical_file_uri,
    html,
    graph,
):
    query_string = build_update_decision_document_html_query(
        decision_document_uri,
        logical_file_uri,
        html,
        graph,
        datetime.now(timezone.utc),
    )

    update(query_string)


def update_task_status(task_uri, status, graph):
    query_string = build_update_task_status_query(
        task_uri,
        status,
        graph,
        datetime.now(timezone.utc),
    )

    update(query_string)