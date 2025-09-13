from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

# ------------------------------
# Mensaje individual
# ------------------------------
class Message(BaseModel):
    """
    Representa un mensaje en la conversación.
    
    Attributes:
        role: Rol del mensaje, 'user' o 'bot'.
        message: Contenido textual del mensaje.
    """
    role: Literal["user", "bot"] = Field(..., description="Rol del mensaje: 'user' o 'bot'.")
    message: str = Field(..., description="Contenido del mensaje.")


# ------------------------------
# Request de la API
# ------------------------------
class ChatRequest(BaseModel):
    """
    Representa el request para iniciar o continuar una conversación.
    
    Attributes:
        conversation_id: ID de la conversación existente. Si no se envía, se inicia una nueva conversación.
        message: Mensaje del usuario.
    """
    conversation_id: Optional[str] = Field(None, description="ID de la conversación existente. Omitir para nueva conversación.")
    message: str = Field(..., description="Mensaje del usuario.")


# ------------------------------
# Link HATEOAS
# ------------------------------
class Link(BaseModel):
    """
    Representa un enlace HATEOAS.
    
    Attributes:
        rel: Tipo de relación (ej. 'self', 'continue', 'new').
        href: URL del recurso relacionado.
    """
    rel: str = Field(..., description="Tipo de relación (ej. 'self', 'continue', 'new').")
    href: str = Field(..., description="URL del recurso relacionado.")


# ------------------------------
# Response de la API
# ------------------------------
class ChatResponse(BaseModel):
    """
    Representa la respuesta de la API de conversación.
    
    Attributes:
        conversation_id: ID único de la conversación.
        messages: Lista de mensajes intercambiados en la conversación.
        links: Lista de enlaces para navegación de la API.
    """
    conversation_id: str = Field(..., description="ID único de la conversación.")
    messages: List[Message] = Field(..., description="Lista de mensajes de la conversación.")
    links: Optional[List[Link]] = Field([], description="Enlaces para navegación de la API.")
