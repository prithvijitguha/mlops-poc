"""
This module, `app.py`, is the main entry point for the Hei! InsightAssist application.

The application uses the OpenAI GPT-3.5-turbo model to provide a natural language interface for querying data from a SQLite database. The application is built with Streamlit and uses the Llama Index library for natural language processing and the Pygwalker library for data visualization.

The application provides a chat interface where users can input natural language queries. The queries are processed by the OpenAI model and converted into SQL queries, which are then executed against the SQLite database. The results are displayed in the chat interface and, if requested by the user, visualized using Pygwalker.

The application also includes error handling for failed SQL queries and a debug mode for chart configuration.

Functions:
    get_pyg_renderer(dataframe: pd.DataFrame) -> "StreamlitRenderer":
        Returns an instance of Pygwalker's renderer for data visualization.

This module is part of the Hei! InsightAssist project.
"""

from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine

from utils import setup_db_llm, generate_sql_query, MODEL_NAME
import streamlit as st
import time

from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd

# Read the SQLite path from the test.py file
sql_lite_path = "sqlite:///src/web/data/dataset_all"

# Adjust the width of the Streamlit page
st.set_page_config(page_title="Hei! InsightAssist", layout="wide")


sql_query_engine, sql_database, engine = setup_db_llm()

# Establish communication between pygwalker and streamlit
init_streamlit_comm()


# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer(dataframe: pd.DataFrame) -> "StreamlitRenderer":
    # When you need to publish your app to the public,
    # you should set the debug parameter to False
    # to prevent other users from writing to your chart configuration file.
    return StreamlitRenderer(dataframe, spec="./gw_config.json", debug=False)

from sqlalchemy import create_engine, MetaData



# Create an engine that stores data in the local directory's SQLite database
engine = create_engine(sql_lite_path)

# Create a MetaData instance
metadata = MetaData()

# Reflect the tables from the database
metadata.reflect(bind=engine)


# Display the metadata
metadata_string = ""

# Establish connection with the database
# Then iterate over the tables and display them
with engine.connect() as conn:
    metadata_string = "\n".join([f"- Table Name: **{tb_name}**" for tb_name in metadata.tables])


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display default greeting if chat history is empty
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": f"""Hello! I am Hei!InsightsAssistant. I will help you get insights on the data in your project.

The following tables are available in the database:

{metadata_string}

Here are some example questions you can ask:

- **Tell me about the data**
- **What are the highest selling products in the state of California?**
- **How many active employees are present? i.e., not terminated.**
- **How many male vs female employees**"""
    })

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # We check if 'visualize' in the sql, then we pass the sql generated query
        # to pygwalker to display the dataset                                                                                                                                                                                                                                                                                                                                                              # then we query it
        if (
            "visualize" in prompt.lower()
        ):  # Lowercase the prompt to make it case insensitive
            # We also can't pass visualize to the query engine since it takes too much time and
            # we don't need the response, we just need the query
            # So instead we use our own wrapper function to get the query
            generated_sql_query = generate_sql_query(prompt)
            print("Generated SQL Query: ", generated_sql_query)
            # Then we pass the query to pandas read sql query to get the dataframe
            # We pass the dataframe to the pygwalker renderer
            try:
                with engine.connect() as conn:
                    df = pd.read_sql_query(generated_sql_query, conn)
                    # We get the pygwalker renderer instance
                    renderer = get_pyg_renderer(dataframe=df)
                    # Finally let's render the data exploration interface
                    # Render your data exploration interface. Developers can use it to build charts by drag and drop.
                    renderer.render_explore()
            # If the query is not successful, we use the query engine to get the response
            except (
                Exception
            ) as e:  # TODO: Add specific exception for failure in sql execution
                print(e)
                for chunk in "Error generating visualization, please retry".split():
                    full_response += chunk + " "
                    time.sleep(0.05)
                    # Add a blinking cursor to simulate typing
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
        else:
            # If there is no visualize in the prompt, we pass it to the query engine
            # We get the user input
            # Let's pass it to the query engine to get the response
            response = sql_query_engine.query(prompt)
            # Once we get the response let's log it for debugging
            print(response)
            # Now's lets parse the response
            return_response = response.response  # We need the syntax answer as well
            generated_sql_query = response.metadata[
                "sql_query"
            ]  # We need to get the query part of it
            # In this case would be more 'definitive' answer set
            for chunk in return_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
