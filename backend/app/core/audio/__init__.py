
from typing import Optional

import config
from fastapi import Depends

from .transcriber import AudioTranscriber
from ..agent import get_openai_client, OpenAI

__transcriber: Optional[AudioTranscriber] = None


def get_transcriber(
    openai_client: OpenAI = Depends(get_openai_client)
) -> AudioTranscriber:
    """
    Get the document processor instance.
    """
    global __transcriber
    if not __transcriber:
        __transcriber = AudioTranscriber(openai_client)
    return __transcriber
