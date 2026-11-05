import os
from pathlib import Path

PREFIXES = """
PREFIX task: <http://redpencil.data.gift/vocabularies/tasks/>
PREFIX nie: <http://www.semanticdesktop.org/ontologies/2007/01/19/nie#>
PREFIX nfo: <http://www.semanticdesktop.org/ontologies/2007/03/22/nfo#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX adms: <http://www.w3.org/ns/adms#>
PREFIX lpdc: <http://data.lblod.info/vocabularies/lpdc/>
"""


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

PDF_MIME_TYPE = "application/pdf"
HTML_MIME_TYPES = {
    "text/html",
    "application/xhtml+xml",
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

HTML_ALLOWED_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "p", "br",
    "strong", "em", "b", "i", "u",
    "ul", "ol", "li",
    "dl", "dt", "dd",
    "table", "thead", "tbody", "tr", "th", "td", "caption",
    "figure", "figcaption",
    "blockquote",
    "pre", "code",
    "div", "span",
}

HTML_ALLOWED_ATTRIBUTES = {
    "*": {"colspan", "rowspan"},
}
