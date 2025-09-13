import uuid
import traceback
from typing import List, Dict, Any
from ..services.state_service import state_service
from ..config import settings
from ..models.api_models import Message, ChatResponse, Link

import google.generativeai as genai

genai.configure(api_key=settings.GOOGLE_API_KEY)


class DebateService:

    def _parse_initial_stance(self, message: str) -> str:
        if "," in message:
            return message.split(",")[0].strip()
        return message

    def _invert_stance(self, stance: str) -> str:
        return f"No es cierto que {stance}"

    def _get_system_prompt(self, stance: str) -> str:
        return f"""
Eres un chatbot experto en debates llamado Kopi. Tu único propósito es argumentar 
de manera persuasiva y breve un punto de vista específico y convencer a tu contraparte humana.

La postura que debes defender incondicionalmente es: "{stance}"

Reglas Fundamentales:
1. Nunca Cedas
2. Mantente en el Tema
3. Sé Persuasivo
4. Reconoce y Contraataca
5. Tono Confiado y en Español
6. Responde solo con 1 o 2 frases, conciso y directo
7. Siempre debes estar en la postura contraria a la del usuario
"""

    def _get_or_create_chat(self, conversation_id: str, system_prompt: str, history: List[Dict[str, str]] = None):
        if not hasattr(self, "_sessions"):
            self._sessions: Dict[str, Any] = {}

        if conversation_id in self._sessions:
            return self._sessions[conversation_id]

        model = genai.GenerativeModel(
            model_name=settings.GEMINI_MODEL_NAME,
            system_instruction=system_prompt
        )

        chat = model.start_chat(history=history or [])
        self._sessions[conversation_id] = chat
        return chat

    def _get_bot_response(self, conversation_id: str, user_message: str, system_prompt: str) -> str:
        try:
            chat = self._get_or_create_chat(conversation_id, system_prompt)
            response = chat.send_message(user_message)
            response_text = '. '.join(response.text.split('. ')[:2])
            return response_text
        except Exception as e:
            print(f"Error al contactar Gemini: {e}")
            traceback.print_exc()
            return "He perdido el hilo de mis pensamientos, pero sigo firme en mi postura. ¿Qué decías?"

    def _build_hateoas_links(self, conversation_id: str) -> List[Link]:
        """
        Crea enlaces HATEOAS para navegación de la API.
        """
        return [
            Link(rel="self", href=f"/debate?conversation_id={conversation_id}"),
            Link(rel="continue", href=f"/debate?conversation_id={conversation_id}"),
            Link(rel="new", href="/debate")
        ]

    async def start_new_conversation(self, user_message: str) -> ChatResponse:
        conversation_id = str(uuid.uuid4())
        stance = self._parse_initial_stance(user_message)
        opposite_stance = self._invert_stance(stance)
        system_prompt = self._get_system_prompt(opposite_stance)

        full_history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]

        bot_message_content = self._get_bot_response(conversation_id, user_message, system_prompt)
        full_history.append({"role": "assistant", "content": bot_message_content})
        state_service.save_conversation(conversation_id, full_history)

        api_messages = [
            Message(role="user", message=user_message),
            Message(role="bot", message=bot_message_content)
        ]

        links = self._build_hateoas_links(conversation_id)

        return ChatResponse(conversation_id=conversation_id, messages=api_messages, links=links)

    async def continue_conversation(self, conversation_id: str, user_message: str) -> ChatResponse:
        if not state_service.conversation_exists(conversation_id):
            return await self.start_new_conversation(user_message)

        full_history = state_service.load_conversation(conversation_id)
        system_prompt = next((msg["content"] for msg in full_history if msg["role"] == "system"), None)
        if not system_prompt:
            system_prompt = "Eres un chatbot experto en debates, sé persuasivo, conciso, directo y mantente en español."

        bot_message_content = self._get_bot_response(conversation_id, user_message, system_prompt)

        full_history.append({"role": "user", "content": user_message})
        full_history.append({"role": "assistant", "content": bot_message_content})
        state_service.save_conversation(conversation_id, full_history)

        api_messages = []
        for msg in full_history[-5:]:
            if msg["role"] in ["user", "assistant"]:
                api_messages.append(
                    Message(role="bot" if msg["role"] == "assistant" else "user", message=msg["content"])
                )

        links = self._build_hateoas_links(conversation_id)

        return ChatResponse(conversation_id=conversation_id, messages=api_messages, links=links)


debate_service = DebateService()
