
from typing import Optional

import openai
from openai import OpenAI

import config

__openai_client: Optional[OpenAI] = None

def chat_with_openai(messages):
    try:
        response = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            tools=tools,
            tool_choice='auto')
        response_message = response.choices[0].message
        if response_message.tool_calls:
            messages.append(response_message)
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                if function_name == 'ai_search':
                    result = ai_search(args['skills'], args['neighbors'])
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'name': tool_call.function.name,
                        'content': str(result)
                    })
            second_response = openai.chat.completions.create(
                model='gpt-4o-mini',
                messages=messages,
                tools=tools,
                tool_choice='auto')
            return second_response.choices[0].message.content
        else:
            return response_message.content
    except Exception as e:
        return f"Error: {e}"


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
