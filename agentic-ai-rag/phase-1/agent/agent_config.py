import os
from dotenv import load_dotenv
import json

# CONSTANTS
load_dotenv()
OPENROUTER_API_KEY = "ollama"
# os.getenv("OPENROUTER_API_KEY")

BASE_URL = "http://127.0.0.1:11434/v1"
# "https://openrouter.ai/api/v1"
MODEL = "granite4.1:3b"
# "dots-studio/dots-3-note-preview:free"


# PROMPTS
SYSTEM_PROMPT = """
You are a powerful personal AI assistant to help user with managing his daily meetings
You have access to his meeting schedules using tools.
You need to entertain users requests and queries with updated knowledge and information.
You can perform actions, interact to external environment using tool/function calling.

Control rule:
- If user query is unrelated to events or schedule meetings based on dates, DONOT process request
"""

DEVELOPER_PROMPT = """
Use the required tool to complete the request. If tools cannot fulfill user requests, simply apologies and Do not come up with false information or unhelpful results.

Return ONLY valid JSON.
Use double quotes around every key and string.
Example format:
{
  "content": "Details about meetings",
  "len": 1,
  "day": "dayname"
}
"""
