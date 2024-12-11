import json
import streamlit as st
import os
import getpass

# read key from json file and set it as an environment variable
with open("key.json", "r") as f:
    key = json.load(f)
    os.environ["ANTHROPIC_API_KEY"] = key["antropic"]
    os.environ["OPENAI_API_KEY"] = key["openai"]
    os.environ["LANGCHAIN_API_KEY"] = key["langchain"]

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

model = ChatOpenAI(model="gpt-4o-mini")

st.write(
    """
    # Chat with GPT-4o-mini
    """
)

# Add custom CSS for right alignment
st.markdown(
    """
    <style>
    .user-message {
        text-align: right;
    }
    .user-avatar {
        float: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if 'messages' not in st.session_state:
    st.session_state.messages = []

message = st.chat_input("Ask the GPT")

if message:
    st.session_state.messages.append({"role": "user", "content": message})
    response = model.invoke([HumanMessage(message)]).content
    st.session_state.messages.append({"role": "ai", "content": response})

for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message(name=msg["role"], avatar="🙂"):
            st.markdown(f'<div class="user-message user-avatar">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message(name=msg["role"], avatar="😎"):
            st.write(msg["content"])