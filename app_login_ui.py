import streamlit as st 
import json
from pathlib import Path
import datetime
import uuid
import time

st.set_page_config(
    page_title = "Course Manager",
    page_icon = "",
    layout = "centered",
    initial_sidebar_state = "collapsed"
)

users = (
    {
    "id": "1",
    "email": "admin@school.edu",
    "full_name": "System Admin",
    "password": "123ssag@43AE",
    "role": "Admin",
    "registered_at": "..."
}
)

json_path = Path("users.json")

if json_path.exists():
    with json_path.open("r") as f:
        users = json.load(f)


#initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None


#Login page function
def login_page():
    st.title("Course Manager - Login")

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type = "password")
        submit_btn = st.form_submit_button("Login")

    if submit_btn:
        user = next((u for u in users if u["email"] == email), None)

        if user and user ["password"] == password:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.error("Invalid email or password")


#Dashboard pages
def admin_dashboard():
    st.title("Admin Dashboard")
    st.write(f"Welcome, {st.session_state.user['full_name']}")
    