"""This module details all helper functions for the application"""
from openai import OpenAI
from dotenv import load_dotenv
import os
from llama_index.core import SQLDatabase
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI as llamaOpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine

load_dotenv()  # take environment variables from .env.

MODEL_NAME = "gpt-3.5-turbo"


def setup_db_llm(model=MODEL_NAME):
    """Set up the database connection and the LLM model

    Args:
        model: str: The model name to use for the LLM. Default is "gpt-3.5-turbo"

    Returns:
        sql_query_engine: llama_index.core.query_engine.NLSQLTableQueryEngine
        sql_database: llama_index.core.SQLDatabase
        engine: sqlalchemy.engine.base.Engine
    """
    llm = llamaOpenAI(temperature=0.1, model=model)
    # We setup the database connections here
    engine = create_engine("sqlite:///src/web/data/dataset_all")

    sql_database = SQLDatabase(engine, include_tables=["retail", "hr"])

    sql_query_engine = NLSQLTableQueryEngine(
        sql_database=sql_database, tables=["retail", "hr"], llm=llm
    )

    return sql_query_engine, sql_database, engine


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
