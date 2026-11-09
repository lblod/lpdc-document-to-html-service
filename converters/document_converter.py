from abc import ABC, abstractmethod
from pathlib import Path

class DocumentConverter(ABC):
    @abstractmethod
    def convert_to_html(self, source_path: Path) -> str:
        """Convert a document to HTML."""