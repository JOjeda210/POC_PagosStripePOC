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
- ✅ **Validación automática** - Pydantic para validación de datos
- ✅ **Documentación automática** - Swagger UI integrado (FastAPI por defecto)
- ✅ **Variables de entorno** - Configuración segura
- ✅ **Logging** - Sistema de registro para auditoría

## 📁 Estructura del Proyecto

```
PoC Stripe/
├── src/
│   ├── __init__.py           # Paquete principal
│   ├── main.py              # Aplicación FastAPI principal
│   └── stripe_service.py    # Servicio de integración con Stripe
├── venv/                   # Entorno virtual de Python
├── .env                   # Variables de entorno (no versionar)
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
   STRIPE_SECRET_KEY=sk_test_your_secret_key_here
   STRIPE_PUBLISHABLE_KEY=pk_test_your_publishable_key_here
   STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here
   
   # FastAPI Configuration
   DEBUG=True
   HOST=localhost
   PORT=8000
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

### Endpoints implementados:

| Método | Endpoint | Descripción | Parámetros |
|--------|----------|-------------|------------|
| `GET` | `/` | Endpoint de bienvenida | Ninguno |
| `POST` | `/pay` | Crear un Payment Intent | `amount`, `currency`, `payment_method` |
| `GET` | `/paymentMethods` | Crear método de pago de prueba | Ninguno |
| `POST` | `/refund` | Procesar un reembolso | `payment_id` |
| `GET` | `/status/{payment_id}` | Obtener estado de un pago | `payment_id` (path) |

### Modelos de datos:

#### PaymentRequest
```json
{
  "amount": 2000,
  "currency": "usd",
  "payment_method": ""
}
```

#### RefundRequest
```json
{
  "payment_id": "pi_1234567890"
}
```

### Ejemplos de uso:

#### 1. Crear un Payment Intent
```bash
curl -X POST "http://localhost:8000/pay" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 2000,
    "currency": "usd",
    "payment_method": ""
  }'
```

#### 2. Obtener método de pago de prueba
```bash
curl -X GET "http://localhost:8000/paymentMethods"
```

#### 3. Consultar estado de pago
```bash
curl -X GET "http://localhost:8000/status/pi_1234567890"
```

#### 4. Procesar reembolso
```bash
curl -X POST "http://localhost:8000/refund" \
  -H "Content-Type: application/json" \
  -d '{
    "payment_id": "pi_1234567890"
  }'
```

## 🧪 Testing

### Datos de prueba de Stripe

Utiliza estas tarjetas de prueba:

| Número | Descripción |
|--------|-------------|
| `4242424242424242` | Visa - Pago exitoso |
| `4000000000000002` | Visa - Tarjeta declinada |
| `4000000000009995` | Visa - Fondos insuficientes |

### Limitaciones de montos
- **Mínimo**: $0.50 (50 centavos)
- **Máximo**: $999,999.99

### Monedas soportadas
- `usd`, `eur`, `gbp`, `cad`, `aud`, `jpy`

## 🔒 Seguridad

### Características de seguridad implementadas:

- ✅ **Variables de entorno** para claves API
- ✅ **Validación de entrada** con Pydantic
- ✅ **Validación de montos y monedas**
- ✅ **Manejo seguro de errores**
- ✅ **Logging detallado** para auditoría
- ✅ **Verificación de formato de claves** Stripe

### ⚠️ Importante:

- Las claves API se leen desde variables de entorno
- Todas las operaciones son validadas antes de enviar a Stripe
- Los errores son capturados y loggeados apropiadamente
- Solo se usan claves de prueba en desarrollo

## 📖 Documentación

### Funciones principales:

- **`main.py`**: Define los endpoints de FastAPI y maneja requests/responses
- **`stripe_service.py`**: Contiene toda la lógica de integración con Stripe
- **Validaciones**: Montos, monedas, IDs de pago y claves API
- **Logging**: Registro de todas las operaciones para debugging

### Enlaces útiles:

- [Documentación de Stripe](https://stripe.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Stripe Testing](https://stripe.com/docs/testing)

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