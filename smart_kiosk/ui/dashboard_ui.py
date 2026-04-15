import streamlit as st

def dashboard_render():
    inventory = st.session_state["inventory"]
    orders = st.session_state["orders"]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Inventory", len(inventory))
    with col2:
        st.metric("Total Orders", len(orders))

