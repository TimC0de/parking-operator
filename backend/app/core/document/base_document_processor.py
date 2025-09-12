from abc import ABC, abstractmethod
from typing import Optional

from fastapi import UploadFile


class BaseDocumentProcessor(ABC):
    """
    Base class for document processors.
    """

    def __init__(self):
        pass

    @abstractmethod
    async def process(self, document: UploadFile, sub_paths: Optional[list[str]] = None) -> str:
        """
        Process the document.

        Args:
            document: The document to process.
            sub_paths: Optional subdirectories to create within the upload directory.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_absolute_url_from_path(self, path: str) -> str:
        """
        Get the absolute URL from the given path.

        Args:
            path (str): The path to the document.
        """
        raise NotImplementedError("Subclasses must implement this method.")