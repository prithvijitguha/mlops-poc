from sqlalchemy import Table, Column, Integer, String, Date, Float, create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

Base = declarative_base()
metadata_obj = MetaData()

# Define the Retail table
retail = Table(
    "retail",
    metadata_obj,
    Column("row_id", String, primary_key=True, comment="Unique identifier for each row"),
    Column("order_id", String, comment="Unique identifier for each order"),
    Column("order_date", Date, comment="Date when the order was placed"),
    Column("ship_date", Date, comment="Date when the order was shipped"),
    Column("ship_mode", String, comment="Mode of shipment"),
    Column("customer_id", String, comment="Unique identifier for each customer"),
    Column("customer_name", String, comment="Name of the customer"),
    Column("segment", String, comment="Customer segment"),
    Column("country", String, comment="Country of the customer"),
    Column("city", String, comment="City of the customer"),
    Column("state", String, comment="State of the customer"),
    Column("postal_code", String, comment="Postal code of the customer"),
    Column("region", String, comment="Region of the customer"),
    Column("product_id", String, comment="Unique identifier for each product"),
    Column("category", String, comment="Category of the product"),
    Column("sub_category", String, comment="Sub-category of the product"),
    Column("product_name", String, comment="Name of the product"),
    Column("sales", Float, comment="Sales amount"),
    Column("quantity", Integer, comment="Quantity of the product ordered"),
    Column("discount", Float, comment="Discount applied"),
    Column("profit", Float, comment="Profit amount"),
    comment="A table containing retail data for Walmart USA, detailing the orders and their details"
)

# Define the HR table
hr = Table(
    "hr",
    metadata_obj,
    Column("Employee_Name", String, comment="Name of the employee"),
    Column("EmpID", String, primary_key=True, comment="Unique identifier for each employee"),
    Column("MarriedID", String, comment="Marital status ID"),
    Column("MaritalStatusID", String, comment="Marital status description"),
    Column("GenderID", String, comment="Gender ID"),
    Column("EmpStatusID", String, comment="Employment status ID"),
    Column("DeptID", String, comment="Department ID"),
    Column("PerfScoreID", String, comment="Performance score ID"),
    Column("FromDiversityJobFairID", String, comment="Diversity job fair ID"),
    Column("Salary", Float, comment="Salary of the employee"),
    Column("Termd", String, comment="Termination status"),
    Column("PositionID", String, comment="Position ID"),
    Column("Position", String, comment="Position title"),
    Column("State", String, comment="State of the employee"),
    Column("Zip", String, comment="Zip code of the employee"),
    Column("DOB", Date, comment="Date of birth of the employee"),
    Column("Sex", String, comment="Gender of the employee"),
    Column("MaritalDesc", String, comment="Marital status description"),
    Column("CitizenDesc", String, comment="Citizenship description"),
    Column("HispanicLatino", String, comment="Hispanic/Latino status"),
    Column("RaceDesc", String, comment="Race description"),
    Column("DateofHire", Date, comment="Date of hire"),
    Column("DateofTermination", Date, comment="Date of termination"),
    Column("TermReason", String, comment="Reason for termination"),
    Column("EmploymentStatus", String, comment="Employment status"),
    Column("Department", String, comment="Department name"),
    Column("ManagerName", String, comment="Name of the manager"),
    Column("ManagerID", String, comment="Unique identifier for the manager"),
    Column("RecruitmentSource", String, comment="Source of recruitment"),
    Column("PerformanceScore", String, comment="Performance score"),
    Column("EngagementSurvey", Float, comment="Engagement survey score"),
    Column("EmpSatisfaction", Float, comment="Employee satisfaction score"),
    Column("SpecialProjectsCount", Integer, comment="Count of special projects"),
    Column("LastPerformanceReview_Date", Date, comment="Date of the last performance review"),
    Column("DaysLateLast30", Integer, comment="Days late in the last 30 days"),
    Column("Absences", Integer, comment="Number of absences"),
    comment="A table containing HR data for Walmart USA, detailing the employees and their details"
)

def setup_db():
    """This function is used to setup the database connection and create tables with metadata."""
    # Create an engine that stores data in the local directory's
    engine = create_engine("sqlite:///dataset_all")

    # Create all tables
    metadata_obj.create_all(engine)

    # Load data from CSV files into DataFrames
    retail_df = pd.read_csv("RetailDataset_v2.csv")
    hr_df = pd.read_csv("HRDataset_v15.csv")

    # Write data to the database
    retail_df.to_sql("retail", engine, if_exists="replace", index=False)
    hr_df.to_sql("hr", engine, if_exists="replace", index=False)

setup_db()
