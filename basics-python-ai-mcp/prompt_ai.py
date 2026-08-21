from groq import Groq
import os

client = Groq()


def AI(input: str):
    return client.chat.completions.create(
        model="groq/compound-mini",
        messages=[
            {
                "role": "system",
                "content": "Generate a professional email requesting a one-week extension for a project deadline.",
            },
            {
                "role": "user",
                "content": """
             Write in a professional tone.
            Keep the email between 120–150 words.
            Include a clear subject line.
            Explain the reason politely.
            Propose a new deadline.
            End with a courteous closing.
            Do not make up company names or personal details—use placeholders like [Manager Name].
             """,
            },
            {
                "role": "user",
                "content": input,
            },
        ],
        temperature=0.6,
        max_completion_tokens=2048,
        top_p=0.90,
        # reasoning_effort="none",
        stream=False,
        stop=None,
    )


completion_simple = AI("Project is about AI effecting daily life")
print((completion_simple.choices[0].message.content))

# print("--=======--=======--======--")
# completion_minimum = AI(
#     "Write up about samsung mobiles. Listing their tops smartphones. Sales and comptitors"
# )

# print((completion_minimum.choices[0].message.content))
