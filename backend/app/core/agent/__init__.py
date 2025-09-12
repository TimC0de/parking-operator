
from typing import Optional
from openai import OpenAI

import config

__openai_client: Optional[OpenAI] = None


def get_openai_client(
) -> OpenAI:
    """
    Get the document processor instance.
    """
    global __openai_client
    if not __openai_client:
        __openai_client = OpenAI(
            api_key=config.env_param('OPENAI_API_KEY')
        )
    return __openai_client
