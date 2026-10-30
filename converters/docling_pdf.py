import os
import time
from pathlib import Path

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import (
    DocumentConverter as DoclingDocumentConverter,
    PdfFormatOption,
)

from converters.document_converter import DocumentConverter


class DoclingPdfConverter(DocumentConverter):
    def __init__(self) -> None:
        artifacts_path = os.getenv("DOCLING_ARTIFACTS_PATH")

        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = False

        if artifacts_path:
            pipeline_options.artifacts_path = Path(artifacts_path)

        self._converter = DoclingDocumentConverter(
            allowed_formats=[InputFormat.PDF],
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                ),
            },
        )

    def convert_to_html(self, source_path: Path) -> str:
        source_path = Path(source_path)

        if not source_path.is_file():
            raise FileNotFoundError(
                f"PDF file does not exist: {source_path}"
            )

        with source_path.open("rb") as source_file:
            if not source_file.read(5).startswith(b"%PDF-"):
                raise ValueError(
                    f"Input is not a valid PDF file: {source_path}"
                )

        start = time.perf_counter()
        result = self._converter.convert(source=source_path)
        convert_seconds = time.perf_counter() - start

        if result.document is None:
            raise RuntimeError(
                f"Docling produced no document for: {source_path}"
            )

        start = time.perf_counter()
        html = result.document.export_to_html()
        export_seconds = time.perf_counter() - start

        print(
            f"Docling conversion of {source_path.name}: "
            f"convert={convert_seconds:.2f}s, "
            f"html export={export_seconds:.2f}s, "
            f"total={convert_seconds + export_seconds:.2f}s",
            flush=True,
        )

        return html