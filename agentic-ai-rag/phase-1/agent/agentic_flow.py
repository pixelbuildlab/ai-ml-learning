from agent_config import (
    DEVELOPER_PROMPT,
    SYSTEM_PROMPT,
)
from agent_tools import tools, handle_tool_calls, reflection
from memory.service import save_message
from agent_llm import AI

# MAIN
MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "developer", "content": DEVELOPER_PROMPT},
]


async def agentic_flow(user_query: str, convo_id: int, messages_history: list):
    try:
        MESSAGES.extend(messages_history)

        MESSAGES.append(
            {"role": "user", "content": user_query},
        )
        await save_message(convo_id, "user", user_query)

        count = 1
        while True:
            count += 1

            print("[agent] Starting agentic flow...")

            ai_response = await AI(messages=MESSAGES, tools=tools)
            print("[agent] Agent responded...")

            assistant_reply = ai_response.choices[0].message.model_dump()

            MESSAGES.append(assistant_reply)

            parsed = ai_response.model_dump()
            parsed_message = parsed["choices"][0].get("message")

            assistant_message_content = parsed_message.get("content")

            if assistant_message_content:
                await save_message(convo_id, "assistant", assistant_message_content)

            if count > 3:
                return assistant_reply

            if tool_call := parsed_message.get("tool_calls"):
                print("[agent] Tool calling...")
                func_to_call = tool_call[0].get("function")
                tool_call_id = tool_call[0].get("id")
                tool_call_name = func_to_call.get("name")
                tool_call_args = func_to_call.get("arguments")

                tool_output = handle_tool_calls(tool_call_name, tool_call_args)
                tool_output_content = (
                    f"Function metadata: {tool_output.get("metadata")}."
                    f"Function completion status: {tool_output.get("success")}."
                    f"Function Response: {tool_output.get("response")}"
                )

                formatted_tool_output = {
                    "role": "tool",
                    "tool_name": tool_output.get("func_name", tool_call_name),
                    "tool_id": tool_call_id,
                    "content": tool_output_content,
                }

                await save_message(convo_id, "tool", tool_output_content)

                MESSAGES.append(formatted_tool_output)
                continue  # process next LLM call

            # skipping reflection for NOW. But implementation is similar or use LLM call
            # try:
            #     content = json.loads(assistant_reply.get("content") or "{}")
            #     reflection_result = reflection(content.get("len"), content.get("day"))
            #     ref_crr = reflection_result.get("correct")
            #     ref_rsn = reflection_result.get("reason")
            #     if not ref_crr:
            #         print("[agent] Self reflection shows an error")
            #         # print(r[agent] ef_rsn)

            #         MESSAGES.append(
            #             {
            #                 "role": "user",
            #                 "content": (
            #                     "Your response failed validation.\n"
            #                     f"Reason: {ref_rsn}\n"
            #                     "Please generate a corrected response."
            #                 ),
            #             }
            #         )
            #         continue  # report back reflection reports
            #     else:
            #         print("[agent] self reflection is passed")
            # except Exception as exc:
            #     print("[agent] Failed during self reflection", exc)

            return assistant_reply

    except Exception as excep:
        print("[agent] Unhandled exception in agentic flow", excep)
