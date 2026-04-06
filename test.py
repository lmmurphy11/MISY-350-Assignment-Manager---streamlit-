import streamlit as st
import json
from pathlib import Path
from datetime import datetime
import uuid

st.set_page_config(
    page_title="Inventory Management App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# File paths
# ----------------------------
INVENTORY_FILE = Path("inventory.json")
SALES_FILE = Path("sales_log.json")


# ----------------------------
# Helper functions
# ----------------------------
def load_json(file_path, default_data):
    if file_path.exists():
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return default_data
    return default_data


def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_inventory():
    return load_json(INVENTORY_FILE, [])


def save_inventory(inventory):
    save_json(INVENTORY_FILE, inventory)


def load_sales():
    return load_json(SALES_FILE, [])


def save_sales(sales):
    save_json(SALES_FILE, sales)


def find_product_by_id(inventory, product_id):
    for product in inventory:
        if product["id"] == product_id:
            return product
    return None


def low_stock_items(inventory, threshold=5):
    return [item for item in inventory if item["stock"] <= threshold]


# ----------------------------
# Session state
# ----------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "home"

if "role" not in st.session_state:
    st.session_state["role"] = "Employee"


# ----------------------------
# Load data
# ----------------------------
inventory = load_inventory()
sales_log = load_sales()


# ----------------------------
# Sidebar navigation
# ----------------------------
with st.sidebar:
    st.title("Navigation")

    st.session_state["role"] = st.selectbox(
        "Select Role",
        ["Employee", "Shop Owner"],
        index=0 if st.session_state["role"] == "Employee" else 1
    )

    if st.button("Home", key="home_btn", use_container_width=True):
        st.session_state["page"] = "home"
        st.rerun()

    if st.button("Manage Inventory", key="inventory_btn", use_container_width=True):
        st.session_state["page"] = "inventory"
        st.rerun()

    if st.button("Sales", key="sales_btn", use_container_width=True):
        st.session_state["page"] = "sales"
        st.rerun()


# ----------------------------
# HOME PAGE
# ----------------------------
if st.session_state["page"] == "home":
    st.title("Inventory Management Application")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Products", len(inventory))
    with col2:
        total_units = sum(item["stock"] for item in inventory) if inventory else 0
        st.metric("Total Units in Stock", total_units)
    with col3:
        st.metric("Low Stock Items", len(low_stock_items(inventory)))

    st.divider()

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.subheader("Current Catalog")
        if inventory:
            st.dataframe(inventory, use_container_width=True)
        else:
            st.warning("No products in inventory.")

    with col_right:
        st.subheader("Low Stock Alerts")
        low_items = low_stock_items(inventory)
        if low_items:
            for item in low_items:
                st.error(f"{item['name']} is low on stock: {item['stock']} left")
        else:
            st.success("No low-stock items right now.")


# ----------------------------
# INVENTORY PAGE
# ----------------------------
elif st.session_state["page"] == "inventory":
    st.title("Inventory Management")

    if st.session_state["role"] != "Shop Owner":
        st.warning("Only the Shop Owner can add, update, restock, or delete products.")
        if inventory:
            st.dataframe(inventory, use_container_width=True)
        else:
            st.info("No products available.")
    else:
        tab1, tab2, tab3, tab4 = st.tabs([
            "Add Product",
            "Update Price",
            "Restock Product",
            "Delete Product"
        ])

        # Add Product
        with tab1:
            st.subheader("Add New Product")
            with st.form("add_product_form"):
                product_name = st.text_input("Product Name", key="add_name")
                product_category = st.text_input("Category", key="add_category")
                product_price = st.number_input("Price", min_value=0.0, step=0.01, key="add_price")
                product_stock = st.number_input("Starting Stock", min_value=0, step=1, key="add_stock")
                submit_add = st.form_submit_button("Add Product")

                if submit_add:
                    if product_name.strip() == "":
                        st.error("Product name is required.")
                    else:
                        new_product = {
                            "id": str(uuid.uuid4())[:8],
                            "name": product_name.strip(),
                            "category": product_category.strip(),
                            "price": round(product_price, 2),
                            "stock": int(product_stock),
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        inventory.append(new_product)
                        save_inventory(inventory)
                        st.success(f"{product_name} added successfully.")
                        st.rerun()

        # Update Price
        with tab2:
            st.subheader("Update Product Price")
            if inventory:
                product_options = {
                    f"{item['name']} ({item['id']})": item["id"] for item in inventory
                }
                selected_label = st.selectbox("Select Product", list(product_options.keys()), key="price_select")
                selected_id = product_options[selected_label]
                selected_product = find_product_by_id(inventory, selected_id)

                if selected_product:
                    new_price = st.number_input(
                        "New Price",
                        min_value=0.0,
                        step=0.01,
                        value=float(selected_product["price"]),
                        key="new_price"
                    )

                    if st.button("Update Price", key="update_price_btn"):
                        selected_product["price"] = round(new_price, 2)
                        save_inventory(inventory)
                        st.success("Price updated successfully.")
                        st.rerun()
            else:
                st.info("No products available to update.")

        # Restock Product
        with tab3:
            st.subheader("Restock Inventory")
            if inventory:
                product_options = {
                    f"{item['name']} ({item['id']})": item["id"] for item in inventory
                }
                selected_label = st.selectbox("Select Product to Restock", list(product_options.keys()), key="restock_select")
                selected_id = product_options[selected_label]
                selected_product = find_product_by_id(inventory, selected_id)

                if selected_product:
                    restock_amount = st.number_input("Units to Add", min_value=1, step=1, key="restock_amount")

                    if st.button("Restock Product", key="restock_btn"):
                        selected_product["stock"] += int(restock_amount)
                        save_inventory(inventory)
                        st.success(f"{selected_product['name']} restocked successfully.")
                        st.rerun()
            else:
                st.info("No products available to restock.")

        # Delete Product
        with tab4:
            st.subheader("Delete Discontinued Product")
            if inventory:
                product_options = {
                    f"{item['name']} ({item['id']})": item["id"] for item in inventory
                }
                selected_label = st.selectbox("Select Product to Delete", list(product_options.keys()), key="delete_select")
                selected_id = product_options[selected_label]
                selected_product = find_product_by_id(inventory, selected_id)

                if selected_product:
                    st.warning(f"You are about to delete: {selected_product['name']}")
                    if st.button("Delete Product", key="delete_btn"):
                        inventory = [item for item in inventory if item["id"] != selected_id]
                        save_inventory(inventory)
                        st.success("Product deleted successfully.")
                        st.rerun()
            else:
                st.info("No products available to delete.")

        st.divider()
        st.subheader("Current Inventory")
        if inventory:
            st.dataframe(inventory, use_container_width=True)
        else:
            st.warning("No products in inventory.")


# ----------------------------
# SALES PAGE
# ----------------------------
elif st.session_state["page"] == "sales":
    st.title("Employee Sales Page")

    if not inventory:
        st.warning("No inventory available yet.")
    else:
        col1, col2 = st.columns([3, 2])

        with col1:
            st.subheader("Current Catalog")
            st.dataframe(inventory, use_container_width=True)

        with col2:
            st.subheader("Log a Sale")

            product_options = {
                f"{item['name']} ({item['stock']} in stock)": item["id"] for item in inventory
            }
            selected_label = st.selectbox("Select Product Sold", list(product_options.keys()), key="sale_select")
            selected_id = product_options[selected_label]
            selected_product = find_product_by_id(inventory, selected_id)

            if selected_product:
                sale_quantity = st.number_input(
                    "Quantity Sold",
                    min_value=1,
                    step=1,
                    key="sale_quantity"
                )

                if st.button("Record Sale", key="record_sale_btn"):
                    if sale_quantity > selected_product["stock"]:
                        st.error("Not enough stock available for that sale.")
                    else:
                        selected_product["stock"] -= int(sale_quantity)

                        new_sale = {
                            "sale_id": str(uuid.uuid4())[:8],
                            "product_id": selected_product["id"],
                            "product_name": selected_product["name"],
                            "quantity_sold": int(sale_quantity),
                            "sale_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }

                        sales_log.append(new_sale)
                        save_inventory(inventory)
                        save_sales(sales_log)

                        st.success("Sale recorded successfully.")
                        st.rerun()

        st.divider()

        st.subheader("Dangerously Low Stock")
        low_items = low_stock_items(inventory, threshold=5)
        if low_items:
            for item in low_items:
                st.error(f"{item['name']} is running low: only {item['stock']} left")
        else:
            st.success("No dangerously low items.")

        st.divider()

        st.subheader("Sales Log")
        if sales_log:
            st.dataframe(sales_log, use_container_width=True)
        else:
            st.info("No sales logged yet.")