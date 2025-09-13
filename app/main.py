from fastapi import FastAPI, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse
from app.models.api_models import ChatRequest, ChatResponse, Message
from app.services.debate_service import debate_service
from app.services.state_service import state_service
import time

app = FastAPI(
    title="Kopi Debate Bot con AI", 
    description="API para un chatbot que puede sostener un debate y convencer al usuario, con AI.",
    version="1.2.0"
)

# -------------------- Middleware para medir tiempo de respuesta ---------------------
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"[Tiempo de respuesta] {request.url.path} -> {process_time:.3f} s")
    return response

# -------------------- Endpoint principal ---------------------------------------------
@app.post("/debate", response_model=ChatResponse)
async def handle_debate(request: ChatRequest):
    """
    Inicia o continúa un debate.
    Retorna la conversación y links para HATEOAS.
    """
    try:
        if request.conversation_id is None:
            response = await debate_service.start_new_conversation(request.message)
            conv_id = response.conversation_id
        else:
            response = await debate_service.continue_conversation(request.conversation_id, request.message)
            conv_id = request.conversation_id

        links = [
            {"rel": "self", "href": f"/debate?conversation_id={conv_id}"},
            {"rel": "continue", "href": f"/debate?conversation_id={conv_id}"},
            {"rel": "history", "href": f"/debate/history?conversation_id={conv_id}"}
        ]

        return JSONResponse(
            status_code=200,
            content={
                "conversation_id": conv_id,
                "messages": [msg.dict() for msg in response.messages],
                "links": links
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        print(f"[ERROR] {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno.")
    
    
    
    
    

# -------------------- Endpoint de historial ---------------------------------------------
@app.get("/debate/history", response_model=dict)
async def get_last_messages(conversation_id: str = Query(..., description="ID de la conversación")):
    """
    Retorna los últimos 5 mensajes de cada rol ('user' y 'bot') de la conversación.
    Incluye HATEOAS.
    """
    if not state_service.conversation_exists(conversation_id):
        raise HTTPException(status_code=404, detail="Conversación no encontrada")

    full_history = state_service.load_conversation(conversation_id)

    user_msgs = [msg["content"] for msg in full_history if msg["role"] == "user"][-5:]
    bot_msgs = [msg["content"] for msg in full_history if msg["role"] == "assistant"][-5:]

    links = [
        {"rel": "self", "href": f"/debate/history?conversation_id={conversation_id}"},
        {"rel": "continue", "href": f"/debate?conversation_id={conversation_id}"},
    ]

    return JSONResponse(
        status_code=200,
        content={
            "conversation_id": conversation_id,
            "user_messages": [Message(role="user", message=m).dict() for m in user_msgs],
            "bot_messages": [Message(role="bot", message=m).dict() for m in bot_msgs],
            "links": links
        }
    )
