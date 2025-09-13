import json
from typing import List, Dict, Any
import redis

class StateService:
    """
    Servicio para guardar y cargar conversaciones.
    """

    def __init__(self, redis_url: str):
        self.memory_store: Dict[str, List[Dict[str, Any]]] = {}
        self.redis_available = False

        try:
            self.db = redis.from_url(redis_url, decode_responses=True)
            # Test de conexión
            self.db.ping()
            self.redis_available = True
            print("✅ Redis conectado correctamente")
        except Exception as e:
            print(f"⚠️ Redis no disponible, usando almacenamiento en memoria. Error: {e}")
            self.redis_available = False

    def save_conversation(self, conversation_id: str, history: List[Dict[str, Any]]):
        try:
            if self.redis_available:
                self.db.set(conversation_id, json.dumps(history))
            else:
                self.memory_store[conversation_id] = history
        except Exception as e:
            print(f"Error guardando conversación: {e}")
            self.memory_store[conversation_id] = history

    def load_conversation(self, conversation_id: str) -> List[Dict[str, Any]]:
        try:
            if self.redis_available:
                history_json = self.db.get(conversation_id)
                if history_json:
                    return json.loads(history_json)
            return self.memory_store.get(conversation_id, [])
        except Exception as e:
            print(f"Error cargando conversación: {e}")
            return self.memory_store.get(conversation_id, [])

    def conversation_exists(self, conversation_id: str) -> bool:
        try:
            if self.redis_available:
                return self.db.exists(conversation_id) == 1
            else:
                return conversation_id in self.memory_store
        except Exception as e:
            print(f"Error verificando existencia de conversación: {e}")
            return conversation_id in self.memory_store


state_service = StateService(redis_url="redis://localhost:6379")
