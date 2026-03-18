import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid
import time

st.set_page_config("Orders Management App", layout="wide", initial_sidebar_state="expanded")

if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role" : "assistant",
            "content": "Hi! How can I help you?"
        }
    ]



inventory = [
{"id": 1, "name": "Espresso", "price": 2.50, "stock": 40},
{"id": 2, "name": "Latte", "price": 4.25, "stock": 25},
{"id": 3, "name": "Cold Brew", "price": 3.75, "stock": 30},
{"id": 4, "name": "Mocha", "price": 4.50, "stock": 20},
{"id": 5, "name": "Blueberry Muffin", "price": 2.95, "stock": 18}
]


with st.sidebar:
    if st.button("Home", key="home_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()

    if st.button("Orders", key="orders_btn", type="primary", use_container_width=True):
        st.session_state["page"] = "orders"
        st.rerun()

json_path_inventory = Path("inventory.json")
if json_path_inventory.exists():
    with open(json_path_inventory, "r") as f:
        inventory = json.load(f)

json_path_orders = Path("orders.json")
if json_path_orders.exists():
    with open(json_path_orders, "r") as f:
        orders = json.load(f)

else:
    orders = []


if st.session_state["page"] == "home":
    st.markdown("#Orders Management Application - Home Page")
    col1, col2 = st.columns([4,2])
    with col1:
        selected_category = st.radio("Select a List", ["Inventory", "Orders"], horizontal=True)
        if selected_category == "Inventory":
            if len(inventory) > 0:
                st.dataframe(inventory)
            else:
                st.warning("No item in the inventory")
        else:
            if len(orders) > 0:
                st.dataframe(orders)
            else:
                st.warning("No order is recorded yet")
    with col2:
        if selected_category == "Inventory":
            st.metric("Total Inventory", f"{len(inventory)}")
        else:
            st.metric("Total Orders", f"{len(orders)}")

elif st.session_state["page"] == "orders":
    tab1, tab2 = st.tabs(["Add New Order", "Cancel Order"])
    with tab1:
        col1, col2, = st.columns([3,3])

        with col1:
            st.subheader("Add New Order")
            with st.container(border= True):

                selected_item = st.selectbox("Items", options= inventory,
                                            format_func= lambda x:f"{x['name']}, Stock: {x['stock']}")
                
            quantity = st.number_input("Quantity", min_value=1, step=1)

            if st.button("Create Order", key="create_order_btn", type="primary", use_container_width=True):
                with st.spinner("Creating the order..."):
                    total = quantity * selected_item["price"]
                    
                    for item in inventory:
                        if item["id"] == selected_item["id"]:
                            item["stock"] = item["stock"] - quantity
                            break

                    orders.append(
                        {
                        "id": str(uuid.uuid4()),
                        "item_id": selected_item["id"],
                        "quantity": quantity,
                        "status": "Placed",
                        "total": total
                        }
                    )

                    with open(json_path_inventory, "w") as f:
                        json.dump(inventory, f)
                    
                    with open(json_path_orders, "w") as f:
                        json.dump(orders, f)

                    st.balloons()

                    time.sleep(5)
                    st.session_state["page"] = "home"
                    st.rerun()

        with col2:
            st.subheader("Chatbox - AI Assistant")
            col11, col22 = st.columns([2,2])
            with col11:
                st.caption("Try Asking: How can I add a new order?")
            with col22:
                pass


            with st.container(border=True, height=250):
                for message in st.session_state["messages"]:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])

            user_input = st.chat_input("Ask a question...")
            if user_input:
                with st.spinner("Thinking..."):
                    st.session_state["messages"].append(
                        {
                            "role": "user",
                            "content": user_input
                        }
                    )

                    ai_respose = "I could not find an answer for it, try again!"

                    st.session_state["messages"].append(
                        {
                            "role": "assistant",
                            "content": ai_respose
                        }
                    )

        


    with tab2:
        pass
