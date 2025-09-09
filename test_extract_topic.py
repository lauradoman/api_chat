import pytest
from app.services.debate_service import extract_topic
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.mark.parametrize(
    "text, expected_topic, has_adj",
    [
        ("La programación es divertida", "La programación divertida", True),
        ("El dinero es importante", "El dinero importante", True),
        ("Aprender es bueno", "Aprender", False),
        ("Python es genial", "Python genial", True),
        ("Me gusta la música", "la música", False)
    ]
)
def test_extract_topic(text, expected_topic, has_adj):
    topic, adj_flag = extract_topic(text)
    assert topic.startswith(expected_topic.split()[0])
    assert adj_flag == has_adj
