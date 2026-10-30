from string import Template

from sparql.formatting import (
    sparql_escape_datetime,
    sparql_escape_string,
    sparql_escape_uri,
)


def build_load_task_query(task_uri):
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

    return query_template.substitute(
        task=sparql_escape_uri(task_uri)
    )


def build_load_task_input_files_query(task_uri, graph):
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

                ?logicalFile
                    a nfo:FileDataObject;
                    nfo:fileName ?filename.

                ?physicalFile
                    nie:dataSource ?logicalFile.

                OPTIONAL {
                    ?logicalFile dct:format ?format.
                }
            }
        }
        ORDER BY ?filename
    """)

    return query_template.substitute(
        graph=sparql_escape_uri(graph),
        task=sparql_escape_uri(task_uri),
    )


def build_load_source_documents_query(logical_file_uri, graph):
    query_template = Template("""
        PREFIX dct: <http://purl.org/dc/terms/>

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
    )


def build_update_source_document_html_query(
    source_document_uri,
    logical_file_uri,
    html,
    graph,
    modified,
):
    query_template = Template("""
        PREFIX dct: <http://purl.org/dc/terms/>
        PREFIX lpdcExt: <http://lblod.data.gift/vocabularies/lpdcExt/>

        DELETE {
            GRAPH $graph {
                $sourceDocument lpdcExt:extractedHtml ?oldHtml.
                $sourceDocument dct:modified ?oldModified.
            }
        }
        INSERT {
            GRAPH $graph {
                $sourceDocument lpdcExt:extractedHtml $html.
                $sourceDocument dct:modified $newModified.
            }
        }
        WHERE {
            GRAPH $graph {
                $sourceDocument dct:source $logicalFile.

                OPTIONAL {
                    $sourceDocument lpdcExt:extractedHtml ?oldHtml.
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
    )


def build_update_task_status_query(task_uri, status, graph, modified):
    query_template = Template("""
        PREFIX adms: <http://www.w3.org/ns/adms#>
        PREFIX dct: <http://purl.org/dc/terms/>

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
    )


def build_load_job_of_task_query(task_uri, graph):
    query_template = Template("""
        PREFIX dct: <http://purl.org/dc/terms/>

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
    )
