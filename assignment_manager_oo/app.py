import streamlit as st

from data.assignment_store import AssignmentStore
from services.assignment_manager import AssignmentManager
from ui.assignment_dashboard import AssignmentDashboard

from pathlib import Path

st.set_page_config("Assignment Manager")

st.title("Assignment Manager")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = True

if "role" not in st.session_state:
    st.session_state['role'] = "Instructor"

if "page" not in st.session_state:
    st.session_state['page'] = "dashboard"

if st.session_state["logged_in"]:
    if st.session_state["role"] == "Instructor":
        if st.session_state["page"] == "dashboard":
            store = AssignmentStore(Path("assignment_manager_oo/assignments.json")) #creating an object from the assignment
            manager = AssignmentManager(store.load()) #creating an object from the assignment manager class and setting the inital state of the object
            dashboard = AssignmentDashboard(manager, store)
            dashboard.main() #call the orc

    elif st.session_state["role"] == "Student":
        pass
else:
    pass
    #design/set up log in