from app.config.logging import logging
from enum import Enum
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form

from app.core.document import BaseDocumentProcessor, get_document_processor
from app.core.audio import AudioTranscriber, get_transcriber

router = APIRouter()

logger = logging.getLogger('resolve')


class RequestType(Enum):
    TEXT_REQUEST = "TEXT_REQUEST"
    VOICE_REQUEST = "VOICE_REQUEST"


@router.post(
    "/",
)
async def resolve(
    request_type: RequestType = Form(...),
    request_value: Union[str, UploadFile] = Form(...),
    document_processor: BaseDocumentProcessor = Depends(get_document_processor),
    transcriber: AudioTranscriber = Depends(get_transcriber),
):
    # TODO: Call the agent

    if request_type == RequestType.VOICE_REQUEST:
        logger.info(f'Received CV {request_value.filename}')

        document_path = await document_processor.process(request_value)

        try:
            # Call transcriber
            request_text_value = transcriber.transcribe(document_path)
        except Exception as e:
            return {"response": f"Error transcribing audio: {str(e)}"}
    else:
        request_text_value = request_value

    logger.info(f"Received {request_type} with value: {request_text_value}")

    return {"response": f"Received: {request_text_value}"}