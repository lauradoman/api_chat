import random

# Ejemplos de diccionarios (puedes llenarlos con más frases)
RECOGNITION = [
    "Entiendo tu",
    "Es válido tu",
    "Comprendo tu",
    "Respeto tu",
    "Veo tu",
    "Es comprensible tu",
    "No comparto tu"
]

RECOGNITION2 = [
    "opinion",
    "idea",
    "punto de vista",
    "postura"
]

CONNECTOR = [
    "sin embargo,",
    "por otro lado,",
    "además,",
    "y es interesante,",
    "aunque hay otro lado,",
    "pero vale la pena considerar más ángulos,"
]

SUGGESTION = [
    "quizá",
    "te invito a reflexionar que",
    "considera",
    "examina"
]

ACTION = [
    "la perspectiva sobre",
    "el enfoque hacia",
    "la manera en que analizamos",
]

PLANTEMENT = [
    "puede aportar algo valioso.",
    "abre nuevas posibilidades.",
    "nos ayuda a ampliar horizontes."
    "que no siempre es como parece"
]


def generate_dynamic_response(topic: str, has_adj: bool) -> str:
    """Genera respuesta persuasiva dinámica combinando diccionarios"""
    rec = random.choice(RECOGNITION)
    rec2 = random.choice(RECOGNITION2)
    conn = random.choice(CONNECTOR)
    sugg = random.choice(SUGGESTION)
    act = random.choice(ACTION)
    plant = random.choice(PLANTEMENT)

    if has_adj:
        return f"{rec} {rec2} {conn} {sugg} {act} {topic} {plant}"
    else:
        return f"{rec} {rec2} {conn} {sugg} {act} {topic} para que veas otra perspectiva."


def decide_bot_posture(user_message: str, topic_data: tuple) -> str:
    """Genera respuesta del bot usando plantilla dinámica"""
    topic, has_adj = topic_data
    return generate_dynamic_response(topic, has_adj)
