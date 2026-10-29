from converters.docling_pdf import DoclingPdfConverter
from utils.utils import normalize_mime_type


PDF_MIME_TYPE = "application/pdf"

class UnsupportedMimeTypeError(ValueError):
    pass


def is_supported_mime_type(mime_type: str) -> bool:
    return normalize_mime_type(mime_type) == PDF_MIME_TYPE


def get_converter(mime_type: str):
    if is_supported_mime_type(mime_type):
        return DoclingPdfConverter()

    raise UnsupportedMimeTypeError(
        f"Unsupported MIME type: {mime_type}"
    )