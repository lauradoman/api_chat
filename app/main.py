from fastapi import FastAPI, HTTPException
from app.models.api_models import ChatRequest, ChatResponse, Message
from app.services.debate_service import start_new_conversation, continue_conversation

app = FastAPI(title="Kopi Debate Bot", version="1.0")

@app.post("/chat", response_model=ChatResponse)

def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío.")

    if request.conversation_id:
        chat = continue_conversation(request.conversation_id, request.message)
    else:
        chat = start_new_conversation(request.message)

    response = ChatResponse(
        conversation_id=chat.conversation_id,
        message=[Message(role=m.role, message=m.message) for m in chat.message]
    )
    return response
