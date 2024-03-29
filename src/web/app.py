from utils import call_chat

import streamlit as st
import time


from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
import pandas as pd

# Adjust the width of the Streamlit page
st.set_page_config(
    page_title="Hei! InsightAssist",
    layout="wide"
)


# Establish communication between pygwalker and streamlit
init_streamlit_comm()


# Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
@st.cache_resource
def get_pyg_renderer() -> "StreamlitRenderer":
    df = pd.read_csv("src/web/data/RetailDataset.csv")
    # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
    return StreamlitRenderer(df, spec="./gw_config.json", debug=False)


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

        # Here we call the chat function to get the response from the API
        #assistant_response = call_chat(prompt)


        # First thing we're going to do is to feed the response to the api
        # We get a sql query as response
        # Let's try to execute the query
        # If the query is successful, we get the result and display it
        # If the query is not successful, we use the query engine to get the response
        # If the query engine is not successful, we return an error response to retry n



        # Simulate stream of response with milliseconds delay
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

        # We get the pygwalker renderer instance
        renderer = get_pyg_renderer()
        # Finally let's render the data exploration interface
        # Render your data exploration interface. Developers can use it to build charts by drag and drop.
        renderer.render_explore()
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
