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

#service layer
def build_prompt(context_hint:str):
    return "You are an ai assistant in an online shopping website."\
    "this is for test, so create some example dataset, use it to response"\
    "to the user, if the user is asking about the prior conversations, "\
    "try to reference your answer to the prior conversation"\
    f"this is the context hint {context_hint}"

def get_ai_response(client:OpenAI, chat_history:list, context_hint:str):
    #build prompt
    prompt = build_prompt(context_hint)

    #build promt message
    prompt_message = [
        {
            'role': 'system',
            'content': prompt
        }
    ]

    #build final message
    messages = chat_history + prompt_message

    #call OpenAI
    ai_response = client.chat.completions.create(
        model = "gpt-5-mini",
        messages = messages,
        temperature = 1
    )

    #return repsonse
    return ai_response.choices[0].message.content


#data layer
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

orders = load_orders("ai-assistant/orders.json")
logs = load_logs("ai-assistant/ai_logs.json")

if "messages" not in st.session_state:
    st.session_state['messages'] = []
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
              "role": "assistant",
              "content": "Hi, how can I help you?"
            }
        )

with st.container(border=True, height=400):
    for message in st.session_state['messages']:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state['messages'].append(
        {
            "role": 'user',
            'content': 'user_input'
        }
    )
    with st.chat_message('user'):
        st.markdown(user_input)

    with st.chat_message('assistant'):
        with st.spinner("thinking..."):
            ai_response = get_ai_response(client=client, chat_history=st.session_state['messages'], context_hint="healthcare")

            st.markdown(ai_response)
            st.session_state['message'].append(
                {
                'role': 'assistant',
                'content': ai_response
                }
            )

    log = load_logs("ai_assistant/orders.json")
    logs.append({
        "user_message": user_input,
        "assistant_message": ai_response
    })

    save_logs("ai_assistant/orders.json", logs)