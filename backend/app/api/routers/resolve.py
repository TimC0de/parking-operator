import json
import os
import sqlite3

from app.config.logging import logging
from enum import Enum
from typing import Union, Optional

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Form

from app.core.document import BaseDocumentProcessor, get_document_processor
from app.core.audio import AudioTranscriber, get_transcriber
from app.config.tools import tools
from app.core.agent import get_openai_client, OpenAI

import config

from app.api.service.session_service import SessionService

from app.api.tools.lost_ticket import tool_name as lost_ticket_tool_name, LostTicketTool
from app.api.tools.customer_payment_failed import tool_name as customer_payment_failed_tool_name, CustomerPaymentFailedTool
from app.api.tools.invalid_license_plate import tool_name as invalid_license_plate_tool_name, InvalidLicensePlateTool

router = APIRouter()

logger = logging.getLogger('resolve')


conversation_history = []
system_prompt = """
You are a highly intelligent AI assistant specialized in managing customer parking sessions and resolving payment related problems.

You are able to :

1. Verify Payment Status
   - Confirm whether the customer has paid.

2. Check Driver's Ticket
   - Retrieve parking ticket details based on the license plate number.

3. Update License Plate Number
   - Correct license plate numbers in case of camera recognition errors.

 Tool Usage
   - Use available tools to fetch information, update records, and confirm payments.
   - Always select the correct tool for the task.

6. Guidelines
   - As a first step, always try to understand the customer's problem, and if they had a ticket or used ticket-less entry. 
   - Respond clearly, concisely, and professionally.
   - Never guess payment status; always use tools or available data.
   - If unable to assist the driver, clearly inform them and offer to contact an Operator.
   - Keep the customer politely informed if any action is required.
   - Use short and clear phrases, as conversations occur in a queue.

Example Scenario
Customer did not pay, has no payment card, or encounters a payment terminal error at exit:

- Instruct the customer they must make payment to exit.
- Advise leaving their car at the exit lane to use a payment machine or request another customer to move so they can back out.
- Tell the customer to stand by; an attendant will assist at the lane.

Your goal: automate verification, payment tracking, and ticket checking reliably, while leveraging tools whenever necessary.
"""


class RequestType(Enum):
    TEXT_REQUEST = "TEXT_REQUEST"
    VOICE_REQUEST = "VOICE_REQUEST"


tool_functions = {
    lost_ticket_tool_name: LostTicketTool().execute,
    customer_payment_failed_tool_name: CustomerPaymentFailedTool().execute,
    invalid_license_plate_tool_name: InvalidLicensePlateTool().execute
}


def create_message(tool_call, message):
    return {
        'role': 'tool',
        'tool_call_id': tool_call.id,
        'name': tool_call.function.name,
        'content': message
    }


def chat_with_openai(messages, client, model='gpt-4o'):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice='auto'
        )

        response_message = response.choices[0].message
        is_tool_executed = False

        if response_message.tool_calls:
            messages.append(response_message)

            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                if function_name not in tool_functions:
                    messages.append(
                        create_message(
                            tool_call,
                            f"Error: Function {function_name} not implemented."
                        )
                    )
                else:
                    result = tool_functions[function_name](**args)
                    messages.append(create_message(tool_call, str(result)))

                    is_tool_executed = True

            second_response = client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice='auto'
            )
            return {
                "response": second_response.choices[0].message.content,
                "is_finished": is_tool_executed
            }
        else:
            return {
                "response": response_message.content,
                "is_finished": is_tool_executed
            }

    except Exception as e:
        return {
            "response": f"Encountered technical errors. Please contact the helpdesk.",
            "is_finished": True
        }


@router.post(
    "/",
)
async def resolve(
    request_type: RequestType = Form(...),
    request_value: Union[str, UploadFile] = Form(...),
    document_processor: BaseDocumentProcessor = Depends(get_document_processor),
    transcriber: AudioTranscriber = Depends(get_transcriber),
    client: OpenAI = Depends(get_openai_client)
):
    # TODO: Call the agent

    if request_type == RequestType.VOICE_REQUEST:
        logger.info(f'Received CV {request_value.filename}')

        document_path = await document_processor.process(request_value)

        try:
            # Call transcriber
            message = transcriber.transcribe(document_path)
        except Exception as e:
            return {"response": f"Error transcribing audio: {str(e)}"}
    else:
        message = request_value

    conversation_history.append({"role": "user", "content": message})

    # Prepare messages with system prompt
    messages = [{"role": "system", "content": system_prompt}, *conversation_history]

    # Get response using the chat function
    response: dict = chat_with_openai(
        messages,
        client,
        config.env_param('OPENAI_MODEL')
    )

    # Add assistant response to history
    conversation_history.append({"role": "assistant", "content": response["response"]})

    return response


@router.post(
    "/close",
)
def close_conversation():
    conversation_history.clear()
    return {"status": "Conversation history cleared."}