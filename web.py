from flask import jsonify, request
from flask_executor import Executor

from delta import InvalidDeltaError, extract_scheduled_task_uris
from tasks.task_processor import process_task_candidate

app.config["EXECUTOR_TYPE"] = "thread"
app.config["EXECUTOR_MAX_WORKERS"] = 1

executor = Executor(app)

@app.route("/delta", methods=["POST"])
def delta_handler():
    request_data = request.get_json(silent=True)

    try:
        task_uris = extract_scheduled_task_uris(
            request_data
        )
    except InvalidDeltaError as error:
        return jsonify({"error": str(error)}), 400

    for task_uri in task_uris:
        executor.submit(
            process_task_candidate,
            task_uri,
        )

    if task_uris:
        return "", 202

    return "", 204
