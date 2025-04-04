import streamlit as st
import os
from dotenv import load_dotenv
from src.utils import create_db
from langchain_groq import ChatGroq
from langchain.callbacks.streamlit import StreamlitCallbackHandler
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_sql_agent, AgentType

load_dotenv()

# Set the page configuration
st.set_page_config(
    page_title="Chat bot with SQL DB Data",
    page_icon=":guardsman:",
    layout="wide",
)

st.title("Chat bot with SQL DB Data")
st.write(
    """
    This is a simple chat bot that uses SQL database data to answer questions.
    """
)
localdb="USE_LOCALDB"
mysqldb="USE_MYSQLDB"
# Sidebar for user input
st.sidebar.title("User Input")
radio_option = st.sidebar.radio(
    "Select an option",
    ("Chat with bot using sqlite", "Chat with bot using mysql"),
)

if radio_option == "Chat with bot using sqlite":
    db_uri=localdb
    st.sidebar.write(
        """
        This is a simple chat bot that uses SQLite database data to answer questions.
        """
    )
elif radio_option == "Chat with bot using mysql":
    db_uri=mysqldb
    mysql_host=st.sidebar.text_input(
        "Enter your MySQL connection string (e.g., mysql+pymysql://username:password@localhost/db_name)"
    )
    mysql_table=st.sidebar.text_input(
        "Enter your MySQL table name (e.g., STUDENT)"
    )
    mysql_user=st.sidebar.text_input("Enter your MySQL username")
    mysql_password=st.sidebar.text_input("Enter your MySQL password", type="password")
    
api_key = st.sidebar.text_input("Enter your Groq API key", type="password")

if not db_uri:
    st.sidebar.error("Please select a database option.")
    
if not api_key:
    st.sidebar.error("Please enter your Groq API key.")
    
if db_uri==localdb:
    db=create_db(db_uri)
elif db_uri==mysqldb:
    if not mysql_host or not mysql_user:
        st.sidebar.error("Please enter your MySQL connection details.")
    else:
        db=create_db(db_uri,mysql_host=mysql_host,mysql_user=mysql_user,mysql_db=mysql_table)
    
llm=ChatGroq(model_name="gemma2-9b-it", api_key=api_key)

toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(llm, toolkit, verbose=True, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION)

# Initialize session state for chat history
if "messages" not in st.session_state or st.sidebar.button("Reset"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How can I help you today?"}
    ]

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])    

# User input
user_input = st.chat_input("Ask a question about the database:")
if user_input:
    # Add user message to chat history
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)
    
    with st.chat_message("assistant"):
        st_cb= StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
        # Get response from the agent
        response = agent.run(user_input,callbacks=[st_cb])

    # Add assistant message to chat history
    st.session_state["messages"].append({"role": "assistant", "content": response})

    # Display the assistant's response
    st.chat_message("assistant").write(response)