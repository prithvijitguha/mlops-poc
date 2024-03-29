"""This module details all helper functions for the application"""
from openai import OpenAI
from dotenv import load_dotenv
import os



load_dotenv()  # take environment variables from .env.


def generate_sql_query(question: str, model_name="gpt-3.5-turbo") -> str:
    """This function is used to call the OpenAI/Model Serving endpoint
    We wait for a response and return that. Make sure add a timeout so we don't wait for too long
    or incase server is down for some reason

    Args:
        - question: str: The question to ask the model

    Returns:
        - str: The response from the model
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """Given the following SQL tables, your job is to write queries given a user's request:
                CREATE TABLE Retail (
                    RowID int,
                    OrderID varchar(255),
                    OrderDate date,
                    ShipDate date,
                    ShipMode varchar(255),
                    CustomerID varchar(255),
                    CustomerName varchar(255),
                    Segment varchar(255),
                    Country varchar(255),
                    City varchar(255),
                    State varchar(255),
                    PostalCode int,
                    Region varchar(255),
                    ProductID varchar(255),
                    Category varchar(255),
                    SubCategory varchar(255),
                    ProductName varchar(255),
                    Sales decimal,
                    Quantity int,
                    Discount decimal,
                    Profit decimal,
                    PRIMARY KEY (RowID)
                    );"""
            },
            {
                "role": "user",
                "content": f"Write a SQL query which computes {question}"
            }
        ],
        model=model_name,
        temperature=0.7,
    )

    chat_choices = chat_completion.choices # This is a list of choices returned by the model
    # We select the first choice as the response
    return chat_choices[0].message.content.replace('`', '').split('sql\n')[1]



def run_query():
    """The assumption is we will get an SQL query as output which we can use to query the table
    This is going to run the query and return the result.

    This function must raise an error if its not valid SQL
    """
    raise NotImplementedError
