import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = "sk_test_51RFmUQRrEDMpe1JnI53kr2O9wfRUKfpmvt8OWflTJCHQIiJO6JfRuf969MWozaMYwNkMvfISFk8DbaM48BVpTmgf00WQj0VIfN"

# Base de datos simulada
payments_db = {}

def get_payment_method ():
    payment_method = stripe.PaymentMethod.create(
  type="card",
 card={
     "exp_month" : 12,
     "exp_year" : 2034,
     "number" : "4242424242424242",
     "cvc" : "411",  
    },
  
  billing_details={"name": "John Doe"}
)
    return payment_method

def create_payment_intent(amount: int, currency: str = "usd", payment_method:str=""):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency,payment_method = payment_method,
        automatic_payment_methods={"enabled": True},
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
