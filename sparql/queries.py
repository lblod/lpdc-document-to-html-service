from string import Template

from utils.constants import PREFIXES
from sparql.formatting import (
    sparql_escape_datetime,
    sparql_escape_string,
    sparql_escape_uri,
)


def build_load_task_query(task_uri):
    query_template = Template("""
        $PREFIXES

        SELECT DISTINCT ?graph ?status ?operation
        WHERE {
            GRAPH ?graph {
                $task a task:Task;
                      adms:status ?status;
                      task:operation ?operation.
            }
        }
    """)

    return query_template.substitute(
        task=sparql_escape_uri(task_uri),
        PREFIXES = PREFIXES,
    )


def build_load_task_input_files_query(task_uri, graph):
    query_template = Template("""
        $PREFIXES

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

                OPTIONAL {
                    ?physicalCandidate nie:dataSource ?logicalFile.
                }

                BIND(COALESCE(?physicalCandidate, ?logicalFile) AS ?physicalFile)

                ?physicalFile
                    a nfo:FileDataObject;
                    nfo:fileName ?filename.

                OPTIONAL {
                    ?physicalFile dct:format ?format.
                }
            }
        }
        ORDER BY ?filename
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
        PREFIXES = PREFIXES,
    )


def build_load_source_documents_query(logical_file_uri, graph):
    query_template = Template("""
        $PREFIXES

        SELECT DISTINCT ?sourceDocument
        WHERE {
            GRAPH $graph {
                ?sourceDocument dct:source $logicalFile.
            }
        }
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        logicalFile=sparql_escape_uri(logical_file_uri),
        PREFIXES = PREFIXES,
    )


def build_update_source_document_html_query(
    source_document_uri,
    logical_file_uri,
    html,
    graph,
    modified,
):
    query_template = Template("""
        $PREFIXES

        DELETE {
            GRAPH $graph {
                $sourceDocument lpdc:extractedHtml ?oldHtml.
                $sourceDocument dct:modified ?oldModified.
            }
        }
        INSERT {
            GRAPH $graph {
                $sourceDocument lpdc:extractedHtml $html.
                $sourceDocument dct:modified $newModified.
            }
        }
        WHERE {
            GRAPH $graph {
                $sourceDocument dct:source $logicalFile.

                OPTIONAL {
                    $sourceDocument lpdc:extractedHtml ?oldHtml.
                }

                OPTIONAL {
                    $sourceDocument dct:modified ?oldModified.
                }
            }
        }
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        sourceDocument=sparql_escape_uri(source_document_uri),
        logicalFile=sparql_escape_uri(logical_file_uri),
        html=sparql_escape_string(html),
        newModified=sparql_escape_datetime(modified),
        PREFIXES = PREFIXES,
    )


def build_update_task_status_query(task_uri, status, graph, modified):
    query_template = Template("""
        $PREFIXES

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
                $task adms:status ?oldStatus.

                OPTIONAL {
                    $task dct:modified ?oldModified.
                }
            }
        }
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
        newStatus=sparql_escape_uri(status),
        newModified=sparql_escape_datetime(modified),
        PREFIXES = PREFIXES,
    )


def build_load_job_of_task_query(task_uri, graph):
    query_template = Template("""
        $PREFIXES

        SELECT DISTINCT ?job
        WHERE {
            GRAPH $graph {
                $task dct:isPartOf ?job.
            }
        }
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
        PREFIXES = PREFIXES,
    )
