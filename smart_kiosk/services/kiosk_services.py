import uuid
from typing import Optional, List, Dict

def place_order(inventory: list, orders: list, item_id: str, quantity: int) -> Optional[Dict]:
    #find item in the inventory
    item = find_inventory_item_by_item_id(inventory, item_id)
    #if it exists -> 
    if item:
        if item['stock'] >= quantity:
            item['stock'] = item['stock'] - quantity
            total_cost = item['unit_price'] * quantity

            #if the stock is > the quantity asked
            #reduce the inventory
            #then place the new order
            new_order ={
                "order_id": str(uuid.uuid4()),
                "item_id": item_id,
                "quantity": quantity,
                "status": "placed",
                "total_cost": total_cost
            }
            orders.append(new_order)
            return new_order



def find_inventory_item_by_item_id(inventory: list, item_id: str) -> Optional[Dict]:
    for item in inventory:
        if item['item_id'] == item_id:
            return item
        return None
    

def update_order_status():
    pass

def cancel_order():
    pass

def count_orders_for_item_by_item_id():
    pass