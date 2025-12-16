from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx


app = FastAPI()

# # fastapi dev URLs
# PAYMENT_URL = "http://localhost:5000/checkout"
# CART_URL = "http://localhost:5002/cart/"
# INVENTORY_URL = "http://localhost:5001/inventory/"

# Docker DNS resolved URLs
PAYMENT_URL = "http://payment:5000/checkout"
CART_URL = "http://cart:5000/cart/"
INVENTORY_URL = "http://inventory:5000/inventory/"


@app.put("/inventory/add")
async def add_to_inventory(item: str, quantity: int):
    payload = {"quantity": quantity}

    async with httpx.AsyncClient() as client:
        response = await client.put(INVENTORY_URL + item, json=payload, timeout=5.0)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Inventory service failed")

    return response.json()


@app.get("/inventory")
async def get_inventory(item: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(INVENTORY_URL + item, timeout=5.0)

    if response.status_code == 404:
        return False

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Inventory service failed")

    return response.json()


@app.post("/submit_payment")
async def process_payment(item: str, quantity: int, method: str, amount: float):
    payload = {"item": item, "quantity": quantity, "method": method, "amount": amount}

    async with httpx.AsyncClient() as client:
        response = await client.post(PAYMENT_URL, json=payload, timeout=5.0)

    if response.status_code == 404:
        raise HTTPException(status_code=404, detail=f"Invalid payment type: {method}")

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Payment service failed")

    return response.json()


@app.post("/cart/add_item")
async def add_to_cart(user_id: int, item: str, quantity: int):
    stock_check = await get_inventory(item)

    if not stock_check:
        raise HTTPException(status_code=404, detail=f"Item '{item}' not found")
    if stock_check["stock"] < quantity:
        raise HTTPException(status_code=409, detail=f"insufficient '{item}' stock")

    payload = {"item": item, "quantity": quantity}

    async with httpx.AsyncClient() as client:
        response = await client.post(CART_URL + str(user_id), json=payload, timeout=5.0)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Cart service failed")

    await add_to_inventory(item, -quantity)
    return response.json()


@app.post("/add_test_data")
async def add_test_data():
    await add_to_inventory("Laptop", 5)
    await add_to_inventory("Phone", 10)

    await add_to_cart(1234, "Laptop", 2)
    await add_to_cart(1234, "Phone", 1)

    await process_payment("Laptop", 2, "credit_card", 215.30)
    await process_payment("Phone", 1, "pay_pal", 197.50)
