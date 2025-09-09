from app.services.debate_service import limit_history, Message
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def test_limit_history():
    history = [Message(role="user", message=f"U{i}") for i in range(7)] + \
            [Message(role="bot", message=f"B{i}") for i in range(7)]

    limited = limit_history(history, max_per_role=5)

    user_count = sum(1 for m in limited if m.role == "user")
    bot_count = sum(1 for m in limited if m.role == "bot")
    assert user_count <= 5
    assert bot_count <= 5


    user_messages = [m.message for m in limited if m.role == "user"]
    bot_messages = [m.message for m in limited if m.role == "bot"]
    assert user_messages == ["U2", "U3", "U4", "U5", "U6"]
    assert bot_messages == ["B2", "B3", "B4", "B5", "B6"]

    assert len(limited) == user_count + bot_count
