import os
from pathlib import Path

DEFAULT_GRAPH = (
    os.environ.get("DEFAULT_GRAPH")
    or "http://mu.semte.ch/graphs/public"
)


SHARE_PREFIX = "share://"
SHARE_DIR = Path("/share")


OPERATIONS = {
    "CONVERT_DOCUMENT_TO_HTML": (
        "http://lblod.data.gift/id/jobs/concept/"
        "TaskOperation/documentToHtml"
    ),
}


TASK_STATUSES = {
    "BUSY": (
        "http://redpencil.data.gift/id/concept/"
        "JobStatus/busy"
    ),
    "SCHEDULED": (
        "http://redpencil.data.gift/id/concept/"
        "JobStatus/scheduled"
    ),
    "SUCCESS": (
        "http://redpencil.data.gift/id/concept/"
        "JobStatus/success"
    ),
    "FAILED": (
        "http://redpencil.data.gift/id/concept/"
        "JobStatus/failed"
    ),
}