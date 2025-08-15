import stripe
import os
from dotenv import load_dotenv
import logging
from typing import Optional, Dict, Any

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

# Configuración segura de Stripe API Key
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
if not stripe_secret_key:
    logger.error("STRIPE_SECRET_KEY no está configurada en las variables de entorno")
    raise ValueError("STRIPE_SECRET_KEY es requerida")

if not stripe_secret_key.startswith("sk_"):
    logger.error("STRIPE_SECRET_KEY no tiene el formato correcto")
    raise ValueError("STRIPE_SECRET_KEY debe comenzar con 'sk_'")

stripe.api_key = stripe_secret_key

# Base de datos simulada
payments_db = {}

def validate_amount(amount: int) -> bool:
    """Valida que el monto sea válido"""
    return isinstance(amount, int) and 50 <= amount <= 99999999  # Min $0.50, Max $999,999.99

def validate_currency(currency: str) -> bool:
    """Valida que la moneda sea soportada"""
    supported_currencies = ["usd", "eur", "gbp", "cad", "aud", "jpy"]
    return currency.lower() in supported_currencies

def get_payment_method() -> Optional[Dict[str, Any]]:
    """Crea un método de pago de prueba de forma segura"""
    try:
        payment_method = stripe.PaymentMethod.create(
            type="card",
            card={
                "exp_month": 12,
                "exp_year": 2034,
                "number": "4242424242424242",
                "cvc": "411",  
            },
            billing_details={"name": "John Doe"}
        )
        logger.info(f"Método de pago creado: {payment_method.id}")
        return payment_method
    except stripe.error.StripeError as e:
        logger.error(f"Error al crear método de pago: {str(e)}")
        raise

def create_payment_intent(amount: int, currency: str = "usd", payment_method: str = "") -> Optional[Dict[str, Any]]:
    """Crea un Payment Intent con validaciones de seguridad"""
    try:
        # Validaciones de entrada
        if not validate_amount(amount):
            raise ValueError("Monto inválido. Debe estar entre $0.50 y $999,999.99")
        
        if not validate_currency(currency):
            raise ValueError("Moneda no soportada")
        
        # Crear el Payment Intent
        intent_params = {
            "amount": amount,
            "currency": currency.lower(),
            "automatic_payment_methods": {"enabled": True},
        }
        
        # Agregar método de pago si se proporciona
        if payment_method:
            intent_params["payment_method"] = payment_method
        
        intent = stripe.PaymentIntent.create(**intent_params)
        
        # Guardar en base de datos simulada
        payments_db[intent.id] = {
            "status": intent.status,
            "amount": amount,
            "currency": currency.lower(),
            "created_at": intent.created
        }
        
        logger.info(f"Payment Intent creado: {intent.id}")
        return intent
        
    except stripe.error.StripeError as e:
        logger.error(f"Error de Stripe al crear Payment Intent: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise

def get_payment_status(payment_id: str) -> Optional[Dict[str, Any]]:
    """Obtiene el estado de un pago de forma segura"""
    try:
        if not payment_id or not isinstance(payment_id, str):
            raise ValueError("ID de pago inválido")
        
        intent = stripe.PaymentIntent.retrieve(payment_id)
        
        result = {
            "id": intent.id,
            "status": intent.status,
            "amount": intent.amount,
            "currency": intent.currency
        }
        
        logger.info(f"Estado de pago consultado: {payment_id}")
        return result
        
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Payment Intent no encontrado: {payment_id}")
        raise ValueError("Payment Intent no encontrado")
    except stripe.error.StripeError as e:
        logger.error(f"Error de Stripe: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise

def refund_payment(payment_id: str, amount: Optional[int] = None) -> Optional[Dict[str, Any]]:
    """Procesa un reembolso de forma segura"""
    try:
        if not payment_id or not isinstance(payment_id, str):
            raise ValueError("ID de pago inválido")
        
        # Verificar que el pago existe y está en estado válido para reembolso
        intent = stripe.PaymentIntent.retrieve(payment_id)
        if intent.status not in ["succeeded"]:
            raise ValueError("El pago no puede ser reembolsado en su estado actual")
        
        refund_params = {"payment_intent": payment_id}
        if amount and validate_amount(amount):
            refund_params["amount"] = amount
        
        refund = stripe.Refund.create(**refund_params)
        
        # Actualizar base de datos simulada
        if payment_id in payments_db:
            payments_db[payment_id]["status"] = "refunded"
            payments_db[payment_id]["refund_id"] = refund.id
        
        logger.info(f"Reembolso procesado: {refund.id} para payment: {payment_id}")
        return refund
        
    except stripe.error.InvalidRequestError as e:
        logger.error(f"Error en solicitud de reembolso: {str(e)}")
        raise ValueError("No se puede procesar el reembolso")
    except stripe.error.StripeError as e:
        logger.error(f"Error de Stripe en reembolso: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado en reembolso: {str(e)}")
        raise

def verify_webhook_signature(payload: bytes, sig_header: str) -> bool:
    """Verifica la firma del webhook de Stripe"""
    try:
        webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
        if not webhook_secret:
            logger.error("STRIPE_WEBHOOK_SECRET no configurado")
            return False
        
        stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        return True
        
    except stripe.error.SignatureVerificationError:
        logger.error("Firma de webhook inválida")
        return False
    except Exception as e:
        logger.error(f"Error al verificar webhook: {str(e)}")
        return False
