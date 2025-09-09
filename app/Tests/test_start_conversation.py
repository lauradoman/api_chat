from app.services.debate_service import start_new_conversation

def test_start_new_conversation():
    response = start_new_conversation("La programación es divertida")
    assert response.conversation_id is not None
    assert len(response.message) == 2
    assert response.message[0].role == "user"
    assert response.message[1].role == "bot"
