from agentic_flow import agentic_flow
from asyncio import run

print()
print("Talk to your schedule AI assistant. See your meetings.\n Enter bye to exit")
while True:
    print()
    print(">> ", end="")
    user_query = input()

    if user_query.lower().strip() in ["bye", "by", "exit"]:
        exit(1)
    if not user_query.lower().strip():
        continue

    output = run(agentic_flow(user_query))

    print()
    if output and output.get("content"):
        print(output.get("content"))
