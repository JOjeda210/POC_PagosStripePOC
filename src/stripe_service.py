import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Base de datos simulada
payments_db = {}

def create_payment_intent(amount: int, currency: str = "usd"):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,
        payment_method_types=["card"]
    )
    payments_db[intent.id] = {
        "status": intent.status,
        "amount": amount,
        "currency": currency
    }
    return intent

def get_payment_status(payment_id: str):
    intent = stripe.PaymentIntent.retrieve(payment_id)
    return {
        "id": intent.id,
        "status": intent.status,
        "amount": intent.amount,
        "currency": intent.currency
    }

def refund_payment(payment_id: str):
    refund = stripe.Refund.create(payment_intent=payment_id)
    payments_db[payment_id]["status"] = "refunded"
    return refund
