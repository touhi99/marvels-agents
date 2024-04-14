import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from streamlit_chat import message
from agents import agent_executor_func
from auth import get_auth_url, get_access_token
from urllib.parse import urlparse, parse_qs
from util import check_data_exists
from etl import fetch_data, build_kg
from langchain_community.callbacks.streamlit import (
    StreamlitCallbackHandler,
)
st.set_page_config(layout="wide")

def initialize_session_state():
    if 'code' not in st.session_state:
        st.session_state['code'] = None
    if 'token' not in st.session_state:
        st.session_state['token'] = None
    if 'data_fetched' not in st.session_state:
        st.session_state['data_fetched'] = False

initialize_session_state()


with st.sidebar:
    data_exists = check_data_exists()
    if data_exists:
        use_data = st.button("Use Existing Data")
        fetch_new_data = st.button("Fetch New Data")
        if use_data:
            st.session_state['data_fetched'] = True
            st.success("Using existing data. You can now use the data for further processing.")
        elif fetch_new_data:
            st.markdown(f"[Authenticate Here to Fetch New Data]({get_auth_url()})", unsafe_allow_html=True)
    else:
        st.markdown(f"[Authenticate Here]({get_auth_url()})", unsafe_allow_html=True)
        st.write("No existing data found. Please authenticate to fetch new data.")

    redirect_url = st.text_input("Paste the URL you were redirected to here:")
    if redirect_url:
        parsed_url = urlparse(redirect_url)
        params = parse_qs(parsed_url.query)
        st.session_state['code'] = params.get('code', [None])[0]
        if st.session_state['code']:
            response = get_access_token(st.session_state['code'])
            if 'error' in response:
                st.error(f"Error in token request: {response['error_description']}")
                st.session_state['token'] = None  # Reset token on error
            else:
                token = response['access_token']
                st.session_state['token'] = token
                st.success("Authentication successful! Token stored. Fetching data...")

                fetch_data(st.session_state['token'])
                st.session_state['data_fetched'] = True
                st.success("Data fetched successfully! Building knowledge graph...")

                build_kg()
                st.success("Knowledge built successfully!")

if st.session_state['data_fetched']:
    st.write("Data fetching is complete. You can now get insight from your data.")

    agent_executor = agent_executor_func()

    # Function for conversational chat
    def conversational_chat(query, agent_executor):
        st_callback = StreamlitCallbackHandler(st.container())
        result = agent_executor.invoke({"input": query}, {"callbacks": [st_callback]})

        print(result)
        st.session_state['history'].append((query, result['output']))
        return result['output']

    # Initialize chat history
    if 'history' not in st.session_state:
        st.session_state['history'] = []

    # Initialize messages
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello ! Ask Marvel's agent - MSFxChat about " + "" + " 🤗"]

    if 'past' not in st.session_state:
        st.session_state['past'] = ["Hey ! 👋"]

    # Create containers for chat history and user input
    response_container = st.container()
    container = st.container()

    # User input form
    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Query:", placeholder="Talk to your Graph 👉 (:", key='input')
            submit_button = st.form_submit_button(label='Send')

        if submit_button and user_input:
            output = conversational_chat(user_input, agent_executor)
            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

    # Display chat history
    if st.session_state['generated']:
        with response_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="big-smile")
                message(st.session_state["generated"][i], key=str(i), avatar_style="thumbs")