from typing import List, Optional, Literal
from pydantic import BaseModel

# ------------------------------
# Mensaje individual
# ------------------------------
class Message(BaseModel):
    """
    Representa un mensaje en la conversación.
    role: 'user' o 'bot'
    message: contenido del mensaje
    """
    role: Literal["user", "bot"]
    message: str

# ------------------------------
# Request de la API
# ------------------------------
class ChatRequest(BaseModel):
    """
    Modelo para la solicitud de chat.
    - conversation_id: opcional, si se envía continua conversación
    - message: texto del usuario
    """
    conversation_id: Optional[str] = None
    message: str

# ------------------------------
# Response de la API
# ------------------------------
class ChatResponse(BaseModel):
    """
    Modelo para la respuesta de la API.
    - conversation_id: ID de la conversación
    - message: lista de mensajes recientes (user/bot)
    """
    conversation_id: str
    message: List[Message]
