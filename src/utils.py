"""This module details all helper functions for the application"""


def call_chat():
    """This function is used to call the OpenAI/Model Serving endpoint
    We get a response and return that"""
    raise NotImplementedError

def run_query():
    """The assumption is we will get an SQL query as output which we can use to query the table
    This is going to run the query and return the result.

    This function must raise an error if its not valid SQL
    """
    raise NotImplementedError
