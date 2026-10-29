from utils.constants import OPERATIONS, TASK_STATUSES
from converters.converter_factory import (
    get_converter,
    is_supported_mime_type,
)
from tasks.task_repository import (
    DecisionDocumentNotFoundError,
    TaskInputNotFoundError,
    TaskNotFoundError,
    load_decision_documents_for_file,
    load_task,
    load_task_input_files,
    update_decision_document_html,
    update_task_status,
)
def process_task_candidate(task_uri):
    try:
        task = load_task(task_uri)
        task_graph = task["graph"]
    except TaskNotFoundError:
        print(f"Ignoring unknown task: {task_uri}", flush=True)
        return
    except Exception as error:
        print(f"Failed to load task {task_uri}: {error}", flush=True)
        return

    if task["operation"] != OPERATIONS["CONVERT_DOCUMENT_TO_HTML"]:
        print(
            f"Ignoring task {task_uri}: "
            f"operation {task['operation']} does not match "
            f"{OPERATIONS['CONVERT_DOCUMENT_TO_HTML']}",
            flush=True,
        )
        return

    if task["status"] != TASK_STATUSES["SCHEDULED"]:
        print(
            f"Ignoring task {task_uri}: "
            f"status is {task['status']}, not scheduled",
            flush=True,
        )
        return

    print(f"Accepted document-to-HTML task: {task_uri}", flush=True)

    try:
        update_task_status(
            task_uri,
            TASK_STATUSES["BUSY"],
            task_graph
        )

        input_files = load_task_input_files(task_uri, task_graph)
        prepared_files = []

        for input_file in input_files:
            source_path = input_file["source_path"]
            mime_type = input_file["mime_type"]

            if not mime_type:
                raise ValueError(
                    "Input file has no MIME type: "
                    f"{input_file['logical_file_uri']}"
                )

            if not source_path.is_file():
                raise FileNotFoundError(
                    f"Input file does not exist: {source_path}"
                )

            try:
                with source_path.open("rb"):
                    pass
            except OSError as error:
                raise ValueError(
                    f"Input file is not readable: {source_path}"
                ) from error

            if not is_supported_mime_type(mime_type):
                raise ValueError(
                    f"Unsupported MIME type {mime_type} for "
                    f"{input_file['logical_file_uri']}"
                )

            input_file["decision_document_uris"] = (
                load_decision_documents_for_file(
                    input_file["logical_file_uri"],
                    task_graph
                )
            )

        for input_file in input_files:
            prepared_files.append(
                (input_file, get_converter(input_file["mime_type"]))
            )

        converted_files = []
        for input_file, converter in prepared_files:
            source_path = input_file["source_path"]
            mime_type = input_file["mime_type"]

            print(
                f"Converting input file {source_path} "
                f"with MIME type {mime_type}",
                flush=True,
            )

            html = converter.convert_to_html(source_path)

            if not isinstance(html, str) or not html.strip():
                raise ValueError(
                    f"Converter returned no HTML for {source_path}"
                )

            converted_files.append((input_file, html))

        for input_file, html in converted_files:
            for decision_document_uri in input_file[
                "decision_document_uris"
            ]:
                update_decision_document_html(
                    decision_document_uri,
                    input_file["logical_file_uri"],
                    html,
                    task_graph
                )

            print(
                f"Converted {input_file['source_path']}; "
                f"generated {len(html)} HTML characters",
                flush=True,
            )

        update_task_status(
            task_uri,
            TASK_STATUSES["SUCCESS"],
            task_graph
        )

        print(f"Successfully completed task: {task_uri}", flush=True)

    except TaskInputNotFoundError as error:
        print(f"Task has no usable input files: {error}", flush=True)

        try:
            update_task_status(
                task_uri,
                TASK_STATUSES["FAILED"],
                task_graph
            )
        except Exception as status_error:
            print(
                f"Could not mark task {task_uri} as failed: "
                f"{status_error}",
                flush=True,
            )

    except DecisionDocumentNotFoundError as error:
        print(f"Could not find output decision document: {error}", flush=True)

        try:
            update_task_status(
                task_uri,
                TASK_STATUSES["FAILED"],
                task_graph
            )
        except Exception as status_error:
            print(
                f"Could not mark task {task_uri} as failed: "
                f"{status_error}",
                flush=True,
            )

    except Exception as error:
        print(f"Failed to process task {task_uri}: {error}", flush=True)

        try:
            update_task_status(
                task_uri,
                TASK_STATUSES["FAILED"],
                task_graph
            )
        except Exception as status_error:
            print(
                f"Could not mark task {task_uri} as failed: "
                f"{status_error}",
                flush=True,
            )
