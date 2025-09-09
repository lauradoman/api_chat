from app.services.debate_service import limit_history, Message

def test_limit_history():
    # Creamos un historial de 7 mensajes de cada rol
    history = [Message(role="user", message=f"U{i}") for i in range(7)] + \
            [Message(role="bot", message=f"B{i}") for i in range(7)]

    # Limitamos a 5 mensajes por rol
    limited = limit_history(history, max_per_role=5)

    # Contamos los mensajes por rol
    user_count = sum(1 for m in limited if m.role == "user")
    bot_count = sum(1 for m in limited if m.role == "bot")

    # Validamos que no haya más de 5 por rol
    assert user_count <= 5
    assert bot_count <= 5

    # Validamos que sean los últimos 5 mensajes de cada rol
    user_messages = [m.message for m in limited if m.role == "user"]
    bot_messages = [m.message for m in limited if m.role == "bot"]
    assert user_messages == ["U2", "U3", "U4", "U5", "U6"]
    assert bot_messages == ["B2", "B3", "B4", "B5", "B6"]

    # Validamos la longitud total
    assert len(limited) == user_count + bot_count
