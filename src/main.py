"""The overall main program. In this we would do the following
Take input from user -> call_ai -> get response and run query -> validate

We retry 2 times before telling the user we failed.
"""
from openai import OpenAI
from dotenv import load_dotenv
from utils import call_chat, run_query

import os


load_dotenv()  # take environment variables from .env.

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)


print(chat_completion.choices.content)
print(type(chat_completion))
print(chat_completion)
