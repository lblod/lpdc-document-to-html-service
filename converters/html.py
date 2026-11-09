from pathlib import Path

from converters.document_converter import DocumentConverter


class HtmlConverter(DocumentConverter):
    def convert_to_html(self, source_path: Path) -> str:
        source_path = Path(source_path)

        if not source_path.is_file():
            raise FileNotFoundError(
                f"HTML file does not exist: {source_path}"
            )

        return source_path.read_text(encoding="utf-8")