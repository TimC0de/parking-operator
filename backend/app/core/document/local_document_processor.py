import os
from typing import Optional

from app.core.document.base_document_processor import BaseDocumentProcessor
from fastapi import UploadFile

import config


class LocalDocumentProcessor(BaseDocumentProcessor):
    """
    Local document processor for handling file uploads.
    """

    def __init__(self, upload_directory: str):
        self.upload_directory = upload_directory

    async def process(self, document: UploadFile, sub_paths: Optional[list[str]] = None) -> str:
        """
        Process the document by saving it to a local directory.

        Args:
            document: The document to process.
            sub_paths: Optional subdirectories to create within the upload directory.
        """
        sub_paths = sub_paths or []
        position_directory = os.path.join(self.upload_directory, *sub_paths)
        if not os.path.exists(position_directory):
            os.makedirs(position_directory)

        file_location = os.path.join(position_directory, document.filename)

        with open(file_location, "wb") as buffer:
            buffer.write(await document.read())

        # You can process the description and other form data here
        return file_location

    def get_absolute_url_from_path(self, path: str) -> str:
        """
        Get the absolute URL from the given path.

        Args:
            path (str): The path to the document.
        """
        return config.env_param('APP_BASE') + path