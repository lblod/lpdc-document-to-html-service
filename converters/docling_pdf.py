from pathlib import Path

from converters.base import DocumentConverter


class DoclingPdfConverter(DocumentConverter):
    def convert_to_html(self, source_path: Path) -> str:
        source_path = Path(source_path)

        if not source_path.is_file():
            raise FileNotFoundError(
                f"PDF file does not exist: {source_path}"
            )

        with source_path.open("rb") as source_file:
            header = source_file.read(1024)

        if b"%PDF-" not in header:
            raise ValueError(
                f"Input is not a valid PDF file: {source_path}"
            )

        return "<html><body><p>Flow test</p></body></html>"

