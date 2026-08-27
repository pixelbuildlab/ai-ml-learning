from agentic_flow import agentic_flow
from asyncio import run
from memory.service import (
    init_conversation,
    get_recent_messages,
    process_extracted_memory,
    load_user_memories,
)
from memory.extractor import memory_extract
from agent_startup_config import USER_ID, CONVO_ID


async def main():

    user_id = int(USER_ID) if USER_ID else 1
    print()
    print("""
        📅 Schedule AI Assistant

        • Meeting & schedule lookup
        • Conversation history
        • Long-term memory
        • Self-reflection

        Type 'bye' to exit.
    """)
    print()

    convo_id = (
        await init_conversation(user_id=user_id) if not CONVO_ID else int(CONVO_ID)
    )

    if not convo_id:
        raise Exception("Conversation not yet created")

    messages_history = await get_recent_messages(convo_id)
    print(f"[system] loaded chat history len={len(messages_history)}")

    while True:
        print()
        print(">> ", end="")
        user_query = input()

        if user_query.lower().strip() in ["bye", "by", "exit"]:
            exit(1)

        if not user_query.lower().strip():
            continue

        memory = await memory_extract(user_query)

        if memory and memory.should_remember:
            await process_extracted_memory(memory, user_id)

        user_memories = await load_user_memories(user_id)
        print(user_memories)

        output = await agentic_flow(user_query, convo_id, messages_history)

        print()
        if output and output.get("content"):
            print("-" * 100)
            print()
            print(output.get("content"))


if __name__ == "__main__":
    run(main())
    pass
