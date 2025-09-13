# Mejoras y Hallazgos – CHat API

Durante la prueba y uso del sistema, se identificaron varios aspectos que podrían mejorar la experiencia del usuario y la robustez técnica del bot, las enlisto a continuacino.

1. Rigidez en la Lógica de la Conversación

    - **Repetitividad:** El modelo de generación de respuestas, basado en plantillas, puede volverse repetitivo. Si el usuario insiste en su postura negativa, el bot podría responder con las mismas estructuras (“Entiendo, pero…”, “Comprendo, sin embargo…”), afectando la naturalidad de la conversación.

   - **Falta de Manejo del Cambio de Tema:** Actualmente, el sistema asume que la conversación se mantiene sobre “programación”. No contempla cambios de tema por parte del usuario, por ejemplo, si después de programar el usuario pregunta “¿y qué opinas del cine?”, el bot podría seguir anclado al tema original.

    - **Escalada de la Conversación:** No hay un mecanismo para cuando la contra-perspectiva no funciona. Sería útil considerar:
      - Escalar a un agente basado en algun modelo LLM.

      - Ofrecer recursos adicionales (tutoriales, enlaces, etc.).

     - Terminar la conversación de manera cordial cuando sea necesario.

<br>

2. Simplificación del Procesamiento de Lenguaje Natural (NLP)

    - Pérdida de Matices: Clasificar “difícil”, “aburrido”, "cansado" simplemente como una “postura negativa” es una simplificación. Diferenciar estos matices permitiría respuestas más específicas y útiles.

    - Manejo de Ambigüedad: No se contempla cómo manejar mensajes ambiguos, sarcásticos o preguntas complejas sin postura clara.

<br>

1. Aspectos Técnicos y de Robustez

    - Manejo de Errores: El diagrama actual muestra solo el “camino feliz”. No se especifica qué ocurre si:

        - La librería NLP falla o no puede procesar el texto.
        - La base de datos no está disponible.
        - El mensaje del usuario está vacío o incomprensible.


<br>


# ✅ Recomendaciones y Soluciones Propuestas

Como backend developer, propongo las siguientes mejoras para fortalecer la arquitectura, aumentar la escalabilidad y brindar una experiencia más natural al usuario:

<br>

1. Mejorar la Lógica de la Conversación

Uso de un motor más dinámico: **Integrar un LLM externo** (ej. OpenAI, Cohere) o un modelo propio fine-tuned que permita mayor variedad en las respuestas y reduzca la repetitividad.

Detección de cambio de tema: Implementar un clasificador de tópicos que identifique si el usuario cambió de contexto (ejemplo: de “programación” a “cine”) y ajustar dinámicamente el flujo.

- Estrategia de cierre o escalada: Ofrecer un recurso externo cuando el bot detecte frustración.

 Implementar una opción de “finalizar conversación cordialmente” para no forzar interacciones artificiales.

<br>

2. Enriquecer el Procesamiento de Lenguaje Natural (NLP)

Ampliar el análisis semántico: Usar embeddings semánticos (ej. sentence-transformers) para distinguir entre “difícil”, “aburrido” y “cansado”.

Manejo de ambigüedad y sarcasmo: Entrenar reglas o un clasificador adicional que identifique ironía y preguntas abiertas.

Soporte multilenguaje: Incluir modelos pre-entrenados (ej. es_core_news_md de SpaCy o modelos de HuggingFace) para tener un análisis más rico en español.


<br>

3. Fortalecer Aspectos Técnicos y de Robustez

- Manejo de errores estructurado:

Capturar excepciones de SpaCy u otros módulos con middleware de FastAPI (@app.exception_handler).

Validar entradas antes de procesar (ej. no permitir mensajes vacíos).

- Persistencia del historial:

Usar SQLite/PostgreSQL para almacenar las conversaciones.

Implementar un sistema de resúmenes (ej. almacenar solo las últimas N interacciones o usar embeddings para resumir).

- Entornos y Configuración:

Definir variables en .env (con .env.example).

Separar entornos dev, test, prod para una gestión más clara.

- Escalabilidad:

Implementar colas (ej. RabbitMQ o Redis) si se requieren tiempos de respuesta consistentes.
