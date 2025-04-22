from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src import stripe_service  # Importamos nuestra lógica de Stripe

app = FastAPI()

class PaymentRequest(BaseModel):
    amount: int
    currency: str = "usd"
    payment_method: str = ""

class RefundRequest(BaseModel):
    payment_id: str

@app.get("/")
def root():
    return {"message": "PoC de Stripe funcionando 👌"}

@app.post("/pay")
def pay(req: PaymentRequest):
    try:
        intent = stripe_service.create_payment_intent(req.amount, req.currency,req.payment_method)
        return {
            "payment_id": intent.id,
            "status": intent.status,
            "client_secret": intent.client_secret
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/paymentMethods")
def paymentMethods():
    try:
        intent = stripe_service.get_payment_method()
        return intent
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))    

@app.post("/refund")
def refund(req: RefundRequest):
    try:
        refund = stripe_service.refund_payment(req.payment_id)
        return {"refund_id": refund.id, "status": refund.status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/status/{payment_id}")
def status(payment_id: str):
    try:
        info = stripe_service.get_payment_status(payment_id)
        return info
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
