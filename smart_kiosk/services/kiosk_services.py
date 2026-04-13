import uuid


#Query 1: Place a new order for an item and quantity

#find orders placed for an inventory item using item id

#Step 2: find how many orders placed for the item using item id

#find item information in inventory

def place_order(inventory: list, orders: list, item_id: str, quantity: int):
    #find ite in the inventory
    item = find_inventory_item_by_item_id(inventory, item_id)
    #if it exists -> 
    if item:
        if item['stock'] >= quantity:
            item['stock'] = item['stock'] - quantity
            total_cost = item['unit_price'] * quantity
            new_order ={
                "order_id": str(uuid.uuid4()),
                "item_id": item_id,
                "quantity": quantity,
                "status": "placed",
                "total_cost": total_cost
            }
            orders.append(new_order)
            return new_order

    #if the stock is > the quantity asked
        #reduce the inventory
        #then place the new order
    pass

def find_inventory_item_by_item_id(inventory: list, item_id: str):
    for item in inventory:
        if item['id'] == item_id:
            return item
        return []
    

def update_order_status():
    pass

def cancel_order():
    pass

def count_orders_for_item_by_item_id():
    pass