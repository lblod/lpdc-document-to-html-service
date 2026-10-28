from datetime import datetime, timezone
import json
from pathlib import Path
from string import Template

from sudo_helpers import (
    sparql_escape_datetime,
    sparql_escape_string,
    sparql_escape_uri,
)
from queries import query, update

class TaskNotFoundError(Exception):
    pass


class TaskInputNotFoundError(Exception):
    pass


class DecisionDocumentNotFoundError(Exception):
    pass


def load_task(task_uri):
    query_template = Template("""
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>

        SELECT DISTINCT ?graph ?status ?operation
        WHERE {
            GRAPH ?graph {
                $task a task:Task;
                      adms:status ?status;
                      task:operation ?operation.
            }
        }
    """)

    query_string = query_template.substitute(
        task=sparql_escape_uri(task_uri),
    )

    results = query(query_string)
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


def load_task_input_files(task_uri, graph):
    query_template = Template("""
        PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
        PREFIX nie: <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#>
        PREFIX nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
        PREFIX dct: <http://purl.org/dc/terms/>

        SELECT DISTINCT
            ?container
            ?logicalFile
            ?physicalFile
            ?filename
            ?format
        WHERE {
            GRAPH $graph {
                $task task:inputContainer ?container.

                ?container task:hasFile ?logicalFile.

                ?physicalFile
                    a nfo:FileDataObject;
                    nie:dataSource ?logicalFile;
                    nfo:fileName ?filename.

                OPTIONAL {
                    ?physicalFile dct:format ?format.
                }
            }
        }
        ORDER BY ?filename
    """)

    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
    )

    results = query(query_string)
    bindings = results["results"]["bindings"]

    if not bindings:
        raise TaskInputNotFoundError(
            f"No input files found for task: {task_uri}"
        )

    files = []

    for item in bindings:
        filename = item["filename"]["value"]

        # normally something under /share.
        source_path = Path(filename)

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
    query_template = Template("""
        PREFIX nie: <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#>
        PREFIX lpdcExt: <http://lblod.data.gift/vocabularies/lpdcExt/>

        SELECT DISTINCT ?decisionDocument
        WHERE {
            GRAPH $graph {
                ?decisionDocument a lpdcExt:DecisionDocument;
                                  nie:dataSource $logicalFile.
            }
        }
    """)

    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph),
        logicalFile=sparql_escape_uri(logical_file_uri),
    )

    results = query(query_string)
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
    query_template = Template("""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX nie: <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#>
        PREFIX lpdcExt: <http://lblod.data.gift/vocabularies/lpdcExt/>

        DELETE {
            GRAPH $graph {
                $decisionDocument lpdcExt:extractedHtml ?oldHtml.
                $decisionDocument dct:modified ?oldModified.
            }
        }
        INSERT {
            GRAPH $graph {
                $decisionDocument lpdcExt:extractedHtml $html.
                $decisionDocument dct:modified $newModified.
            }
        }
        WHERE {
            GRAPH $graph {
                $decisionDocument a lpdcExt:DecisionDocument;
                                  nie:dataSource $logicalFile.
                OPTIONAL {
                    $decisionDocument lpdcExt:extractedHtml ?oldHtml.
                }
                OPTIONAL {
                    $decisionDocument dct:modified ?oldModified.
                }
            }
        }
    """)

    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph),
        decisionDocument=sparql_escape_uri(decision_document_uri),
        logicalFile=sparql_escape_uri(logical_file_uri),
        html=sparql_escape_string(html),
        newModified=sparql_escape_datetime(
            datetime.now(timezone.utc)
        ),
    )

    update(query_string)


def update_task_status(task_uri, status, graph):
    query_template = Template("""
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>

        DELETE {
            GRAPH $graph {
                $task adms:status ?oldStatus.
                $task dct:modified ?oldModified.
            }
        }
        INSERT {
            GRAPH $graph {
                $task adms:status $newStatus.
                $task dct:modified $newModified.
            }
        }
        WHERE {
            GRAPH $graph {
                $task a task:Task;
                      adms:status ?oldStatus.

                OPTIONAL {
                    $task dct:modified ?oldModified.
                }
            }
        }
    """)

    query_string = query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
        newStatus=sparql_escape_uri(status),
        newModified=sparql_escape_datetime(
            datetime.now(timezone.utc)
        ),
    )

    update(query_string)