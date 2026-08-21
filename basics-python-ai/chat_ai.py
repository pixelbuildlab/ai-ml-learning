from groq import Groq
import os

print(os.getenv("GROQ_API_KEY"))


client = Groq()

completion = client.chat.completions.create(
    model="qwen/qwen3.6-27b",
    messages=[
        {"role": "system", "content": "Extract the event information in json format"},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday at Mid Avenue Office ",
        },
    ],
    temperature=0.6,
    max_completion_tokens=2048,
    top_p=0.002,
    reasoning_effort="default",
    stream=False,
    stop=None,
    response_format={"type": "json_object"},
)

try:
    if completion.choices[0].message.content:
        import json

        parsed = json.loads(completion.choices[0].message.content)
        print("parse type", type(parsed))
        print(parsed)
        print(parsed.get("location"))
        print(parsed.get("participants"))


except Exception as e:
    print("GOT except")

print(type(completion.choices[0].message.content))
