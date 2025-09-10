# Kopi Debate Bot

Kopi Debate Bot es una API REST construida con **FastAPI** que permite iniciar y continuar conversaciones de debate a través de mensajes de texto. Soporta múltiples conversaciones simultáneas mediante `conversation_id`.

---

## 🗂 Estructura del proyecto

kavak/
│
├─ app/
│ ├─ main.py
│ ├─ models/
│ │ └─ api_models.py
│ └─ services/
│ └─ debate_service.py
│ └─ response_templates.py
├─ Tests/
│ │ └─ test_extract_topic.py
│ │ └─ test_limit_history.py
│ │ └─ test_start_conversation.py
├─ Dockerfile
├─ config.py
├─ encriptado.py
├─ makefile
├─ requerimiento.md
├─ primer-diagrama.jpg
├─ diagrama-funcional.jpg
├─ requirements.txt
└─ README.md

---

## ⚡ Instalación local

1. Clona el repositorio:

```bash
git clone https://github.com/lauradoman/api_chat.git
cd api_chat
```

2. Crea un entorno virtual (opcional pero recomendado):

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Instala las dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Corre la API localmente:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

5. Abre la documentación interactiva de Swagger:

<http://localhost:8000/docs>




# uso con Docker


1. Construye la imagen
```bash
sudo docker build -t kavak_api .
```

2. Corre el contenedor

``` bash
docker run -p 8000:8000 kavak_api .
```

3. La API estara disponible en:

```bash
http://localhost:8000
```

4. Documentacion Swagger en:

```bash
http://localhost:8000/docs
```

# 🔧 Endpoints principales

POST /chat

Envía un mensaje al bot y recibe la respuesta.

Request body (JSON):

```json
{
  "conversation_id": "opcional, string",
  "message": "Hola, quiero debatir sobre inteligencia artificial"
}
```

Response body (JSON):

```json
{
  "conversation_id": "string",
  "message": [
    {
      "role": "bot",
      "message": "Respuesta del bot..."
    }
  ]
}
```
- Si conversation_id está vacío, se inicia una nueva conversación.

- Si se envía un conversation_id, el mensaje se agrega a la conversación existente.

# 📝 Notas

- La API utiliza modelos de datos con Pydantic.

- La lógica de conversación está en app/services/debate_service.py.

- Se puede extender a integración con bases de datos o sistemas de chat en tiempo real.

# 💡 Tips

- Para desarrollo, usa --reload en Uvicorn.

- Para producción, considera usar Gunicorn con Uvicorn workers.

- Para pruebas unitarias, usa pytest.

# 🔗 Links útiles

FastAPI Docs