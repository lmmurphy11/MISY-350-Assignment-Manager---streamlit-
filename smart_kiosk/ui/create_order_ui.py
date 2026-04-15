import streamlit as st
from services import kiosk_services
import time
from data import data_manager
from pathlib import Path

def add_new_order_render():
    inventory = st.session_state["inventory"]
    orders = st.session_state["orders"]

    item_names = []
    for item in inventory:
        item_names.append(item['name'])

    selected_item_name = st.selectbox("Item", item_names, key="item_name_select")
    quantity = st.number_input("Quantity", key="order_quantity_num_input", min_value=0, step=1)
    if st.button("Save Order", key="save_order_btn", type="primary", use_container_width=True):
        with st.spinner("saving..."):
            time.sleep(4)

            #selected_item_item_id
            item_id = None
            for item in inventory:
                item_id = item["item_id"]
                break

            #place order
            if item_id:
                new_order = kiosk_services.place_order(inventory, orders, item_id, quantity)
                if new_order:
                    data_manager.save_data(Path("smart_kiosk/inventory.json"), inventory)
                    data_manager.save_data(Path("smart_kiosk/orders.json"), orders)

                    st.success(f"new order with order id: {new_order['order_id']} is recorded")
                    
                    time.sleep(3)
                    st.rerun()
                else:
                    st.warning("new order was not found")
            else:
                st.warning("item is missing")

    