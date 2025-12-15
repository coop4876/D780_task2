from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# carts dict exist in memory for demo purposes
carts = {}


class CartUpdate(BaseModel):
    item: str
    quantity: int


@app.post("/cart/{user_id}")
async def add_item(user_id: int, update: CartUpdate):
    if user_id not in carts:
        carts[user_id] = {}
    if update.item not in carts[user_id]:
        carts[user_id][update.item] = update.quantity
    else:
        carts[user_id][update.item] += update.quantity
    return {
        "message": {
            "user_id": user_id,
            "item": update.item,
            "quantity": carts[user_id][update.item],
        }
    }


@app.get("/cart/{user_id}")
async def get_cart(user_id: int):
    if user_id in carts:
        return carts[user_id]
    else:
        raise HTTPException(status_code=404, detail=f"User '{user_id}' not found")
