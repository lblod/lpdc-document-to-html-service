import nh3
from html.parser import HTMLParser

from urllib.parse import unquote
from utils.constants import SHARE_DIR, SHARE_PREFIX
from utils.constants import (
    HTML_ALLOWED_ATTRIBUTES,
    HTML_ALLOWED_TAGS,
)

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


def sanitize_html(html: str) -> str:
    return nh3.clean(
        html,
        tags=HTML_ALLOWED_TAGS,
        attributes=HTML_ALLOWED_ATTRIBUTES,
        clean_content_tags={"script", "style", "title"},
        strip_comments=True,
    )

from html.parser import HTMLParser


class _HtmlContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.has_content = False

    def handle_data(self, data):
        if data.strip():
            self.has_content = True

    def handle_starttag(self, tag, attrs):
        if tag in {"img", "table", "figure"}:
            self.has_content = True


def has_html_content(html: str) -> bool:
    parser = _HtmlContentParser()
    parser.feed(html)
    return parser.has_content