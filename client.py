
from openai import OpenAI

client = OpenAI(api_key="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") 

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa & Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message.content)