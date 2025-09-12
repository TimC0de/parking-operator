from typing import Optional

import config

from .base_document_processor import BaseDocumentProcessor
from .local_document_processor import LocalDocumentProcessor

__document_processor: Optional[BaseDocumentProcessor] = None


def get_document_processor() -> BaseDocumentProcessor:
    """
    Get the document processor instance.
    """
    global __document_processor
    if not __document_processor:
        __document_processor = LocalDocumentProcessor(config.env_param('UPLOAD_DIR'))
    return __document_processor
