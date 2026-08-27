from openai import AsyncOpenAI
from agent_config import (
    BASE_URL,
    OPENROUTER_API_KEY,
    MODEL,
)

client = AsyncOpenAI(api_key=OPENROUTER_API_KEY, base_url=BASE_URL)


# METHODS
def AI(messages: list, tools=[], model=None):
    chat_completion = client.chat.completions.create(
        messages=messages, tools=tools, model=model if model else MODEL
    )
    return chat_completion
