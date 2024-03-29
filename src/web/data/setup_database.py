from sqlalchemy import Column, Integer, String, Date, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

import pandas as pd


def setup_db():
    """This function is used to setup the database connection."""
    # Create an engine that stores data in the local directory's
    engine = create_engine('sqlite:///retail.sqlite')

    # Let's read the local csv for retail data
    pd.read_csv("RetailDataset.csv").to_sql("retail.sqlite", engine, if_exists="replace")
    # and store it in the database

    engine2 = create_engine('sqlite:///hr.sqlite')

    pd.read_csv("HRDataset_v14.csv").to_sql("hr.sqlite", engine2, if_exists="replace")

setup_db()
