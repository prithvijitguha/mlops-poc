"""This module details all helper functions for the application"""

from openai import OpenAI
from dotenv import load_dotenv

import os

PROMPT = """You are to retrieve the datasets using a SQL query with the following schema
# ADD SCHEMA HERE
"""

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



def call_chat():
    """This function is used to call the OpenAI/Model Serving endpoint
    We wait for a response and return that. Make sure add a timeout so we don't wait for too long
    or incase server is down for some reason"""
    raise NotImplementedError

def run_query():
    """The assumption is we will get an SQL query as output which we can use to query the table
    This is going to run the query and return the result.

    This function must raise an error if its not valid SQL
    """
    raise NotImplementedError
