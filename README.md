# 🚀 PoC Stripe - FastAPI Integration

Una prueba de concepto (Proof of Concept) que demuestra la integración de **Stripe** con **FastAPI** para el procesamiento de pagos.

## 📋 Tabla de Contenidos

- [🔧 Características](#-características)
- [📁 Estructura del Proyecto](#-estructura-del-proyecto)
- [⚙️ Instalación](#️-instalación)
- [🔑 Configuración](#-configuración)
- [🚀 Uso](#-uso)
- [📚 API Endpoints](#-api-endpoints)
- [🧪 Testing](#-testing)
- [🔒 Seguridad](#-seguridad)
- [📖 Documentación](#-documentación)
- [🤝 Contribución](#-contribución)

## 🔧 Características

- ✅ **FastAPI** - Framework web moderno y rápido para APIs
- ✅ **Stripe Integration** - Procesamiento seguro de pagos
- ✅ **Async/Await** - Operaciones asíncronas para mejor rendimiento
- ✅ **Validación automática** - Pydantic para validación de datos
- ✅ **Documentación automática** - Swagger UI integrado
- ✅ **Webhooks** - Manejo de eventos de Stripe
- ✅ **Variables de entorno** - Configuración segura

## 📁 Estructura del Proyecto

```
PoC Stripe/
├── src/
│   ├── __init__.py           # Paquete principal
│   ├── main.py              # Aplicación FastAPI principal
│   ├── stripe_service.py    # Servicio de integración con Stripe
│   └── readme.md           # Documentación del módulo src
├── venv/                   # Entorno virtual de Python
├── .gitignore             # Archivos ignorados por Git
└── README.md              # Este archivo
```

## ⚙️ Instalación

### Prerrequisitos

- **Python 3.8+**
- **pip** (gestor de paquetes de Python)
- **Cuenta de Stripe** (para las claves API)

### Pasos de instalación

1. **Clona el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd "PoC Stripe"
   ```

2. **Crea y activa el entorno virtual**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # Linux/Mac
   python -m venv venv
   source venv/bin/activate
   ```

3. **Instala las dependencias**
   ```bash
   pip install fastapi uvicorn stripe python-dotenv
   ```

## 🔑 Configuración

1. **Crea un archivo `.env` en la raíz del proyecto:**
   ```env
   # Stripe Configuration
   STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
   STRIPE_SECRET_KEY=sk_test_your_secret_key_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   
   # FastAPI Configuration
   DEBUG=True
   HOST=localhost
   PORT=8000
   
   # Database (si aplica)
   DATABASE_URL=sqlite:///./stripe_poc.db
   ```

2. **Obtén tus claves de Stripe:**
   - Ve a [Stripe Dashboard](https://dashboard.stripe.com/)
   - Navega a `Developers > API keys`
   - Copia las claves de prueba (test keys)

## 🚀 Uso

### Ejecutar la aplicación

```bash
# Desde la raíz del proyecto
cd src
python -m uvicorn main:app --reload --host localhost --port 8000
```

### Acceder a la aplicación

- **API**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Principales endpoints disponibles:

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Endpoint de bienvenida |
| `POST` | `/create-payment-intent` | Crear un Payment Intent |
| `POST` | `/confirm-payment` | Confirmar un pago |
| `GET` | `/payment/{payment_id}` | Obtener detalles de un pago |
| `POST` | `/webhook` | Webhook para eventos de Stripe |

### Ejemplo de uso:

```python
# Crear un Payment Intent
import requests

response = requests.post("http://localhost:8000/create-payment-intent", 
    json={
        "amount": 2000,  # $20.00 en centavos
        "currency": "usd",
        "description": "Compra de prueba"
    }
)

payment_intent = response.json()
print(f"Client Secret: {payment_intent['client_secret']}")
```

## 🧪 Testing

### Ejecutar tests

```bash
# Instalar pytest si no está instalado
pip install pytest pytest-asyncio

# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pip install pytest-cov
pytest --cov=src
```

### Datos de prueba de Stripe

Utiliza estas tarjetas de prueba:

| Número | Descripción |
|--------|-------------|
| `4242424242424242` | Visa - Pago exitoso |
| `4000000000000002` | Visa - Tarjeta declinada |
| `4000000000009995` | Visa - Fondos insuficientes |

## 🔒 Seguridad

### Mejores prácticas implementadas:

- ✅ **Variables de entorno** para claves sensibles
- ✅ **Validación de webhooks** con signatures
- ✅ **HTTPS requerido** en producción
- ✅ **Validación de entrada** con Pydantic
- ✅ **Manejo seguro de errores**

### ⚠️ Importante:

- **Nunca** hardcodees las claves de Stripe en el código
- Usa siempre las **claves de prueba** durante desarrollo
- Implementa **logging** para auditoría
- Valida todos los **webhooks** de Stripe

## 📖 Documentación

### Documentación adicional:

- [Documentación de Stripe](https://stripe.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Stripe Testing](https://stripe.com/docs/testing)

### Estructura del código:

- **`main.py`**: Configuración principal de FastAPI y rutas
- **`stripe_service.py`**: Lógica de negocio para Stripe
- **`.env`**: Variables de configuración (no versionar)

## 🤝 Contribución

1. **Fork** el proyecto
2. Crea una **rama feature** (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

## 📄 Licencia

Este proyecto es una **Prueba de Concepto** con fines educativos.

## 📞 Contacto

**Desarrollador**: Jesús Ojeda  
**Proyecto**: PoC Stripe - FastAPI Integration

---

### 🔗 Enlaces útiles:

- [Stripe Dashboard](https://dashboard.stripe.com/)
- [FastAPI GitHub](https://github.com/tiangolo/fastapi)
- [Stripe Python Library](https://github.com/stripe/stripe-python)

---

**⚡ ¡Listo para procesar pagos con Stripe y FastAPI!**