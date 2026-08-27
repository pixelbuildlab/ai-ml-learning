from memory.database import get_connection

# key                         value
# ────────────────────────────────────────────
# preferred_meeting_start     10:00
# preferred_meeting_duration  30 minutes
# preferred_meeting_days      Monday, Tuesday
# no_meetings_on              Friday
# work_hours                  09:00-17:00
# timezone                    Asia/Karachi


# # # memory
async def create_memory(user_id: int, key: str, value: str):
    try:
        print("[database] Creating memory")

        connection = await get_connection()
        cur = await connection.execute(
            """
            INSERT INTO memories (user_id, key, value)
            VALUES (?, ?, ?)
            """,
            (user_id, key, value),
        )

        await connection.commit()
        await connection.close()
        return cur.lastrowid

    except Exception as e:
        print("[database] Failed to create memory", e)


async def update_memory(user_id: int, key: str, value: str):
    try:
        print("[database] Updating memory")

        connection = await get_connection()
        cur = await connection.execute(
            """
            UPDATE memories
            SET value = ?,
            updated_at = CURRENT_TIMESTAMP
            WHERE key = ?
            AND user_id = ?
            """,
            (value, key, user_id),
        )

        await connection.commit()
        await connection.close()
        return cur.rowcount

    except Exception as e:
        print("[database] Failed to update memory", e)


async def get_memories(user_id: int):
    try:
        print("[database] getting memories")

        connection = await get_connection()
        cur = await connection.execute(
            """
            SELECT *
            FROM memories
            WHERE user_id = ?
            """,
            (user_id,),
        )

        rows = await cur.fetchall()
        await connection.close()

        return rows
    except Exception as e:
        print("[database] Failed to get memories", e)


# # conversation
async def create_conversation(user_id: int):
    try:
        print("[database] Creating conversations")

        connection = await get_connection()
        cur = await connection.execute(
            """
            INSERT INTO conversations (user_id)
            VALUES (?)
            """,
            (user_id,),
        )

        await connection.commit()
        await connection.close()
        return cur.lastrowid

    except Exception as e:
        print("[database] Failed to create conversations", e)


# # messages
async def add_message(conversation_id, role, content):
    try:
        print(f"[database] adding message to convo={conversation_id} for role={role}")

        connection = await get_connection()
        await connection.execute(
            """
            INSERT INTO messages
            (conversation_id, role, content)
            VALUES (?, ?, ?)
            """,
            (conversation_id, role, content),
        )

        await connection.commit()
        await connection.close()

    except Exception as e:
        print("[database] Failed to add message", e)


async def get_message_list(conversation_id: int, limit: int):
    try:
        print(f"[database] getting messages from convo={conversation_id}")

        connection = await get_connection()
        cursor = await connection.execute(
            """
            SELECT content, role
            FROM messages
            WHERE conversation_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (conversation_id, limit),
        )

        rows = await cursor.fetchall()

        return rows

    except Exception as e:
        print("[database] Failed to get message", e)
