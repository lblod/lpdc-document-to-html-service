from urllib.parse import unquote
from utils.constants import SHARE_DIR, SHARE_PREFIX

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