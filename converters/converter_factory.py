from converters.docling_pdf import DoclingPdfConverter
from converters.html import HtmlConverter
from utils.utils import normalize_mime_type
from utils.constants import PDF_MIME_TYPE, HTML_MIME_TYPES
class UnsupportedMimeTypeError(ValueError):
    pass


def is_supported_mime_type(mime_type: str) -> bool:
    normalized = normalize_mime_type(mime_type)

    return normalized == PDF_MIME_TYPE or normalized in HTML_MIME_TYPES


def get_converter(mime_type: str):
    normalized = normalize_mime_type(mime_type)

    if normalized == PDF_MIME_TYPE:
        return DoclingPdfConverter()

    if normalized in HTML_MIME_TYPES:
        return HtmlConverter()

    raise UnsupportedMimeTypeError(
        f"Unsupported MIME type: {mime_type}"
    )