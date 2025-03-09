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
                Retail Table: A table containing retail data for Walmart USA, detailing the orders and their details
                Description:
                Schema:
                |-- row_id: string (nullable = true)
                |-- order_id: string (nullable = true)
                |-- order_date: date (nullable = true)
                |-- ship_date: date (nullable = true)
                |-- ship_mode: string (nullable = true)
                |-- customer_id: string (nullable = true)
                |-- customer_name: string (nullable = true)
                |-- segment: string (nullable = true)
                |-- country: string (nullable = true)
                |-- city: string (nullable = true)
                |-- state: string (nullable = true)
                |-- postal_code: string (nullable = true)
                |-- region: string (nullable = true)
                |-- product_id: string (nullable = true)
                |-- category: string (nullable = true)
                |-- sub-category: string (nullable = true)
                |-- product_name: string (nullable = true)
                |-- sales: string (nullable = true)
                |-- quantity: string (nullable = true)
                |-- discount: string (nullable = true)
                |-- profit: string (nullable = true)

                HR Table:
                Description: Table containing HR data for Walmart USA, detailing the employees and their details
                Schema:
                |-- Employee_Name: string (nullable = true)
                |-- EmpID: string (nullable = true)
                |-- MarriedID: string (nullable = true)
                |-- MaritalStatusID: string (nullable = true)
                |-- GenderID: string (nullable = true)
                |-- EmpStatusID: string (nullable = true)
                |-- DeptID: string (nullable = true)
                |-- PerfScoreID: string (nullable = true)
                |-- FromDiversityJobFairID: string (nullable = true)
                |-- Salary: string (nullable = true)
                |-- Termd: string (nullable = true)
                |-- PositionID: string (nullable = true)
                |-- Position: string (nullable = true)
                |-- State: string (nullable = true)
                |-- Zip: string (nullable = true)
                |-- DOB: date (nullable = true)
                |-- Sex: string (nullable = true)
                |-- MaritalDesc: string (nullable = true)
                |-- CitizenDesc: string (nullable = true)
                |-- HispanicLatino: string (nullable = true)
                |-- RaceDesc: string (nullable = true)
                |-- DateofHire: string (nullable = true)
                |-- DateofTermination: string (nullable = true)
                |-- TermReason: string (nullable = true)
                |-- EmploymentStatus: string (nullable = true)
                |-- Department: string (nullable = true)
                |-- ManagerName: string (nullable = true)
                |-- ManagerID: string (nullable = true)
                |-- RecruitmentSource: string (nullable = true)
                |-- PerformanceScore: string (nullable = true)
                |-- EngagementSurvey: string (nullable = true)
                |-- EmpSatisfaction: string (nullable = true)
                |-- SpecialProjectsCount: string (nullable = true)
                |-- LastPerformanceReview_Date: string (nullable = true)
                |-- DaysLateLast30: string (nullable = true)
                |-- Absences: string (nullable = true)





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
