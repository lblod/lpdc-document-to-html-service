from pathlib import Path
from urllib.parse import unquote

SHARE_PREFIX = "share://"
SHARE_DIR = Path("/share")


def physical_uri_to_path(physical_file_uri):
    if not physical_file_uri.startswith(SHARE_PREFIX):
        raise ValueError(
            f"Unexpected physical file URI: {physical_file_uri}"
        )
    relative = unquote(physical_file_uri[len(SHARE_PREFIX):])
    return SHARE_DIR / relative

def normalize_mime_type(mime_type):
    if not mime_type:
        return mime_type
    return mime_type.split(";", 1)[0].strip().lower()