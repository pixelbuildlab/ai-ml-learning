import json


def handle_tool_calls(func_name, args):
    func_call = tools_func_map.get(func_name)

    if not func_call:
        raise ValueError("Unhandled function call")
    try:

        args = json.loads(args)
        func_response = func_call(**args)
        return {
            "metadata": f"tool call [{func_name}] is successful and output is available in response key",
            "response": func_response,
            "success": True,
            "func_name": func_name,
        }
    except Exception as e:
        print("failed to parse args")
        return {
            "metadata": f"tool call [{func_name}] is unsuccessful. Unable to provide response",
            "success": False,
            "func_name": func_name,
        }


# tools
# placeholder for Calendar API or Calendly
def user_calendar(day: str) -> dict[str, str | list]:
    calendars = {
        "monday": {
            "meetings": [{"title": "Team Standup", "time": "09:00"}],
            "schedules": [{"title": "Focus Time", "start": "10:00", "end": "12:00"}],
        },
        "tuesday": {
            "meetings": [{"title": "Client Meeting", "time": "11:00"}],
            "schedules": [{"title": "Project Work", "start": "13:00", "end": "16:00"}],
        },
        "wednesday": {
            "meetings": [{"title": "Project Review", "time": "14:00"}],
            "schedules": [{"title": "Focus Time", "start": "09:00", "end": "12:00"}],
        },
        "thursday": {
            "meetings": [{"title": "Planning", "time": "10:00"}],
            "schedules": [{"title": "Development", "start": "13:00", "end": "17:00"}],
        },
        "friday": {
            "meetings": [{"title": "Weekly Review", "time": "15:00"}],
            "schedules": [{"title": "Admin Work", "start": "09:00", "end": "11:00"}],
        },
        "saturday": {"meetings": [], "schedules": []},
        "sunday": {"meetings": [], "schedules": []},
    }

    return {
        "day": day,
        **calendars.get(day.lower(), {"meetings": [], "schedules": []}),
    }


tools = [
    {
        "type": "function",
        "function": {
            "name": "user_calendar",
            "description": "Get user calendar and meeting info",
            "parameters": {
                "type": "object",
                "properties": {
                    "day": {
                        "type": "string",
                        "description": "Week day parameter to get calendar data on specified day",
                    }
                },
                "required": ["day"],
            },
        },
    }
]


tools_func_map = {"user_calendar": user_calendar}


def reflection(nb: int, day: str):
    events = user_calendar(day)
    if not events:
        return {
            "correct": False,
            "reason": f"Unable to trackdown events on day [{day}] during self check",
        }

    meetings = events.get("meetings") or []
    schedules = events.get("schedules") or []

    if not isinstance(meetings, str) and not isinstance(schedules, str):
        events_count = len(meetings) + len(schedules)
        if events_count == int(nb):
            return {"correct": True, "reason": None}
        else:
            return {
                "correct": False,
                "reason": "Number of events does not match to said day.",
            }

    return {
        "correct": False,
        "reason": "Failed to process during self reflection",
    }
