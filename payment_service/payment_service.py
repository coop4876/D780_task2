from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()


# payment type validation
class PaymentType(str, Enum):
    credit_card = "credit_card"
    pay_pal = "pay_pal"


class CheckoutDetails(BaseModel):
    item: str
    quantity: int
    method: str
    amount: float


# # Payment Component in Strategy Pattern
class PaymentStrategy:
    # Abstract class for payment strategies
    def pay(self, amount):
        raise NotImplementedError


class CreditCardPayment(PaymentStrategy):
    # Processes payment via credit card
    def pay(self, amount):
        return {"message": f"Processed {amount} via Credit Card."}


class PayPalPayment(PaymentStrategy):
    # Processes payment via PayPal
    def pay(self, amount):
        return {"message": f"Processed {amount} via PayPal."}


@app.post("/checkout")
async def checkout(checkout_details: CheckoutDetails):
    if checkout_details.method == "credit_card":
        payment = CreditCardPayment()
        return payment.pay(checkout_details.amount)
    if checkout_details.method == "pay_pal":
        payment = PayPalPayment()
        return payment.pay(checkout_details.amount)
    return {"message": "Invalid payment type"}
