
# app/services/debate_service.py
import uuid
from typing import List, Dict
import spacy
from app.models.api_models import Message, ChatResponse
from app.services.response_templates import generate_dynamic_response

# --- NLP ---
nlp = spacy.load("es_core_news_sm")  # Modelo español

# --- Historial de conversaciones ---
conversations: Dict[str, List[Message]] = {}
MAX_HISTORY = 5  # últimos 5 mensajes por rol

# --- Funciones de extracción de tema ---

def extract_topic(text: str) -> tuple[str, bool]:
    doc = nlp(text)
    topic = ""
    has_adj = False

    for token in doc:
        # Sustantivo o nombre propio principal
        if token.pos_ in ("NOUN", "PROPN"):
            # Añadir determinantes si existen
            det = " ".join([child.text for child in token.children if child.dep_ == "det"])
            topic = (det + " " + token.text).strip() if det else token.text

            # Adjetivos dependientes del sustantivo
            adj_children = [child.text for child in token.children if child.pos_ == "ADJ"]
            if adj_children:
                topic += " " + " ".join(adj_children)
                has_adj = True
            else:
                # Adjetivo predicativo ligado al verbo "ser"
                for tok in doc:
                    if tok.pos_ == "ADJ" and any(child.dep_ == "cop" and child.lemma_ == "ser" for child in tok.head.children):
                        topic += " " + tok.text
                        has_adj = True
                        break

            return topic, has_adj

    # Si no hay sustantivo principal, devolver los primeros tokens
    return " ".join([t.text for t in doc[:3]]), False



# --- Funciones de decisión de postura ---

def decide_bot_posture(user_message: str, topic_data: tuple) -> str:
    """Genera respuesta del bot usando plantilla dinámica"""
    topic, has_adj = topic_data
    return generate_dynamic_response(topic, has_adj)

# --- Funciones de conversación ---

def start_new_conversation(user_message: str) -> ChatResponse:
    """Inicia conversación nueva"""
    conversation_id = str(uuid.uuid4())
    topic_data = extract_topic(user_message)
    bot_posture = decide_bot_posture(user_message, topic_data)

    user_msg = Message(role="user", message=user_message)
    bot_msg = Message(role="bot", message=bot_posture)

    conversations[conversation_id] = [user_msg, bot_msg]

    return ChatResponse(
        conversation_id=conversation_id,
        message=conversations[conversation_id]
    )


def continue_conversation(conversation_id: str, user_message: str) -> ChatResponse:
    """Continúa conversación existente"""
    if conversation_id not in conversations:
        return start_new_conversation(user_message)

    user_msg = Message(role="user", message=user_message)
    conversations[conversation_id].append(user_msg)

    topic_data = extract_topic(user_message)
    bot_msg = Message(role="bot", message=decide_bot_posture(user_message, topic_data))
    conversations[conversation_id].append(bot_msg)

    conversations[conversation_id] = limit_history(conversations[conversation_id], MAX_HISTORY)

    return ChatResponse(
        conversation_id=conversation_id,
        message=conversations[conversation_id]
    )


def limit_history(history: List[Message], max_per_role: int) -> List[Message]:
    """Limita los mensajes por rol manteniendo orden cronológico"""
    user_msgs = [m for m in history if m.role == "user"][-max_per_role:]
    bot_msgs = [m for m in history if m.role == "bot"][-max_per_role:]

    combined = []
    i, j = 0, 0
    for m in history:
        if m.role == "user" and i < len(user_msgs):
            combined.append(user_msgs[i])
            i += 1
        elif m.role == "bot" and j < len(bot_msgs):
            combined.append(bot_msgs[j])
            j += 1
    return combined
