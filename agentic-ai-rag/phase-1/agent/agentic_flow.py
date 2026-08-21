from openai import AsyncOpenAI
import json
from agent_config import (
    BASE_URL,
    DEVELOPER_PROMPT,
    OPENROUTER_API_KEY,
    SYSTEM_PROMPT,
    MODEL,
)
from agent_tools import tools, handle_tool_calls, reflection

client = AsyncOpenAI(api_key=OPENROUTER_API_KEY, base_url=BASE_URL)


# METHODS
def AI(messages: list, tools=[]):
    chat_completion = client.chat.completions.create(
        messages=messages, tools=tools, model=MODEL
    )
    return chat_completion


# MAIN
MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "developer", "content": DEVELOPER_PROMPT},
]


async def agentic_flow(user_query: str):
    try:
        MESSAGES.append(
            {"role": "user", "content": user_query},
        )
        count = 1
        while True:
            count += 1
            print("Starting agentic flow...")
            ai_response = await AI(messages=MESSAGES, tools=tools)
            print("Agent responded...")

            assistant_reply = ai_response.choices[0].message.model_dump()

            MESSAGES.append(assistant_reply)

            parsed = ai_response.model_dump()
            parsed_message = parsed["choices"][0].get("message")

            if count > 3:
                return assistant_reply

            if tool_call := parsed_message.get("tool_calls"):
                print("Tool calling...")
                func_to_call = tool_call[0].get("function")
                tool_call_id = tool_call[0].get("id")
                tool_call_name = func_to_call.get("name")
                tool_call_args = func_to_call.get("arguments")

                tool_output = handle_tool_calls(tool_call_name, tool_call_args)

                formatted_tool_output = {
                    "role": "tool",
                    "tool_name": tool_output.get("func_name", tool_call_name),
                    "tool_id": tool_call_id,
                    "content": f"Function metadata: {tool_output.get("metadata")}. Function completion status: {tool_output.get("success")}. Function Response: {tool_output.get("response")}",
                }

                MESSAGES.append(formatted_tool_output)
                continue  # process next LLM call

            try:
                content = json.loads(assistant_reply.get("content") or "{}")
                reflection_result = reflection(content.get("len"), content.get("day"))
                ref_crr = reflection_result.get("correct")
                ref_rsn = reflection_result.get("reason")
                if not ref_crr:
                    print("Self reflection shows an error")
                    print(ref_rsn)

                    MESSAGES.append(
                        {
                            "role": "user",
                            "content": (
                                "Your response failed validation.\n"
                                f"Reason: {ref_rsn}\n"
                                "Please generate a corrected response."
                            ),
                        }
                    )
                    continue  # report back reflection reports
                else:
                    print("self reflection is passed")
            except Exception as exc:
                print("Failed during self reflection", exc)
                pass

            return assistant_reply

    except Exception as excep:
        print("Unhandled exception in agentic flow", excep)
