import streamlit as st
import json
import os
from datetime import datetime


data_file = "requests.json"

#functions

def load_requests():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []


def save_requests(requests):
    with open(data_file, "w") as file:
        json.dump(requests, file, indent=4)

def generate_requests_id(requests):
    return str(111212 + len(requests) + 1)


#setup

st.set_page_config(page_title= "Excused Absence App", layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "selected_request" not in st.session_state:
    st.session_state.selected_request = None

requests = load_requests()


#sidebar

st.sidebar.title("Navigation")

if st.sidebar.button("Excused Absence Dashboard", key="nav_dashboard"):
    st.session_state.page = "Dashboard"
    st.rerun()

if st.sidebar.button("Excused Absence Requests", key="nav_requests"):
    st.session_state.page = "Request"
    st.rerun()


#dashboard
if st.session_state.page == "Dashboard":
    st.title("Excused Absence Dashboard")

    if len(requests) == 0:
        st.info("No excused absence requests have been submitted.")
    else:
        st.subheader("All Requests")

        event = st.dataframe(
            requests,
            on_select="rerun",
            selection_mode="single-row",
            use_container_width=True,
        )

        if event.selection.rows:
            selected_index = event.selection.rows[0]
            st.session_state.selected_request = requests[selected_index]

        if st.session_state.selected_request:
            selected_request = st.session_state.selected_request

            st.subheader("Selected Request Details")
            st.write(f"**Request ID:** {selected_request['request_id']}")
            st.write(f"**Status:** {selected_request['status']}")
            st.write(f"**Course ID:** {selected_request['course_id']}")
            st.write(f"**Student Email:** {selected_request['student_email']}")
            st.write(f"**Absence Date:** {selected_request['absence_date']}")
            st.write(f"**Submitted Timestamp:** {selected_request['submitted_timestamp']}")
            st.write(f"**Excuse Type:** {selected_request['excuse_type']}")
            st.write(f"**Explanation:** {selected_request['explanation']}")
            st.write(f"**Instructor Note:** {selected_request['instructor_note']}")

            st.subheader("Update Status / Instructor Note")

            new_status = st.selectbox(
                "Update Status",
                ["Pending", "Approved", "Cancelled"],
                index=["Pending", "Approved", "Cancelled"].index(selected_request["status"]),
                key="dashboard_status_select"
            )

            new_note = st.text_area(
                "Instructor Note",
                value=selected_request["instructor_note"],
                key="dashboard_instructor_note"
            )

