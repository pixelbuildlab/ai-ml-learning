from memory.repository import (
    create_conversation,
    add_message,
    get_message_list,
    get_memories,
    create_memory,
    update_memory,
)
from data_types import Memory


async def process_extracted_memory(memory: Memory, user_id: int):
    existing_memory = await get_memories(user_id)

    existing_memory = [
        dict(row)
        for row in (existing_memory or [])
        if dict(row).get("key") == memory.key
    ]

    assert memory.key is not None
    assert memory.value is not None

    if not existing_memory:
        await create_memory(user_id, memory.key, memory.value)
    else:
        await update_memory(user_id, memory.key, memory.value)


async def load_user_memories(user_id: int):

    memories = await get_memories(user_id)
    memories = [dict(row) for row in memories or []]
    return memories


async def init_conversation(user_id: int):
    return await create_conversation(user_id)


async def save_message(
    conversation_id: int,
    role: str,
    content: str,
):
    return await add_message(
        conversation_id,
        role,
        content,
    )


async def get_recent_messages(conversation_id: int, limit: int = 10):
    message_list = await get_message_list(conversation_id, limit)
    print([dict(row) for row in message_list or []])
    list_content = []
    if message_list:
        for item in message_list:
            list_content.append({"content": item[0], "role": item[1]})

    return list_content
