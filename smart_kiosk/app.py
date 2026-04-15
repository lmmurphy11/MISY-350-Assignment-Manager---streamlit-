import streamlit as st

from pathlib import Path

from data import data_manager

st.set_page_config("Smart Kiosk")

st.header("Smart Kiosk")

if "inventory"not in st.session_state:
    st.session_state["inventory"] = data_manager.load_data(Path("smart_kiosk/inventory.json"))

if "orders" not in st.session_state:
    st.session_state["orders"] = data_manager.load_data(Path("smart_kiosk/orders.json"))

with st.sidebar:
    st.markdown("## Smart Kiosk")

tab1, tab2 = st.tabs(["Dashboard", "Add New Order"])

with tab1:
    from ui import dashboard_ui
    dashboard_ui.dashboard_render()

with tab2:
    from ui import create_order_ui
    create_order_ui.add_new_order_render()