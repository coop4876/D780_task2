from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# inventory dict and observer list exist in memory for demo purposes
inventory = {}
observers = []


class InventoryUpdate(BaseModel):
    quantity: int


@app.get("/inventory/{item}")
async def get_item(item: str):
    if item not in inventory:
        raise HTTPException(
            status_code=404, detail=f"Item '{item}' not found in inventory"
        )
    return {"item": item, "stock": inventory[item]}


@app.put("/inventory/{item}")
async def add_item(item: str, update: InventoryUpdate):
    if item not in inventory:
        inventory[item] = update.quantity
        notify_observers(item)
    else:
        inventory[item] += update.quantity
        notify_observers(item)
    return {"message": item + " stock updated."}


@app.put("/inventory/observer/{observer_id}")
async def add_observer(observer_id: str):
    observer = InventoryObserver(observer_id)
    observers.append(observer)
    return {"message": "Inventory observer registered"}


class InventoryObserver:
    def __init__(self, id):
        self.id = id

    def notify(self, item, quantity):
        print(f"Observer ID {self.id} Notification: {item} stock is now {quantity}.")


def notify_observers(item):
    for observer in observers:
        observer.notify(item, inventory[item])
