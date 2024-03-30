from utils import generate_sql_query
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase
from llama_index.llms.openai import OpenAI
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.core.query_engine import PandasQueryEngine

import streamlit as st
import time

from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd

MODEL_NAME = "gpt-3.5-turbo"

# Adjust the width of the Streamlit page
st.set_page_config(page_title="Hei! InsightAssist", layout="wide")

llm = OpenAI(temperature=0.1, model=MODEL_NAME)

# engine = create_engine('sqlite:///src/web/data/retail')
engine = create_engine("sqlite:///src/web/data/dataset_all")

sql_database = SQLDatabase(engine, include_tables=["retail", "hr"])

sql_query_engine = NLSQLTableQueryEngine(
    sql_database=sql_database, tables=["retail", "hr"], llm=llm
)

# Establish communication between pygwalker and streamlit
init_streamlit_comm()


# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer(dataframe: pd.DataFrame) -> "StreamlitRenderer":
    # When you need to publish your app to the public,
    # you should set the debug parameter to False
    # to prevent other users from writing to your chart configuration file.
    return StreamlitRenderer(dataframe, spec="./gw_config.json", debug=False)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

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

        # We check if 'visualize' in the sql, then we pass the sql generated query
        # to pygwalker to display the dataset                                                                                                                                                                                                                                                                                                                                                              # then we query it
        if (
            "visualize" in prompt.lower()
        ):  # Lowercase the prompt to make it case insensitive
            print("Generated SQL Query: ", generated_sql_query)
            try:
                # If the query is successful, we get the result and display it
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
            # If we don't have 'visualize' in the prompt, we return the response
            # In this case would be more 'definitive' answer set
            for chunk in return_response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                # Add a blinking cursor to simulate typing
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)


    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
