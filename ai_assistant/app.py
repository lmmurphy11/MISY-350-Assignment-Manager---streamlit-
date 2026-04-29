import os 
import streamlit as st

#make sure to install apckages if it shows error
#pip install load_dotenv
#pip install OpenAI
from dotenv import load_dotenv
from openai import OpenAI

import json
from pathlib import Path

load_dotenv()

st.set_page_config("AI Assistant - Open AI")
st.title("AI Assistant - Open AI")

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("Open Ai key was not found")
    st.stop()

client = OpenAI(api_key=api_key) #creating an objust from the openAI class and 
                                 #initializing it with my openAI key

#def layer
def load_orders(filepath: str): 
    json_path = Path(filepath)
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return[]


# load logs
def load_logs(filepath: str):
    json_path = Path(filepath)
    if json_path.exists():
        with open(json_path, "r") as f:
            return json.load(f)
    else:
        return[]
    
# save logs
def save_logs(filepath: str, logs: list):
    json_path = Path(filepath)
    with open(json_path, "w") as f:
        json.dump(logs, f)


if "messages" not in st.session_state:
    st.session_state['messages'] = []


orders = load_orders("ai-assistant/orders.json")
logs = load_logs("ai-assistant/ai_logs.json")

for log in logs:
    st.session_state['messages'].append(
        {
            "role": log['role'],
            "content": log["content"]
        }
    )

if len(logs) == 0:
    st.session_state['messages'].append(
        {
            "role": "ai-assistant",
            "content": "Hi, how can I help you?"
        }
    )

with st.container(border=True, height=400):
    for message in st.session_state['messages']:
        with st.container(border=True):
            with st.chat_message(message['role']):
                st.markdown(message['content'])