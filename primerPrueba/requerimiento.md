# 📌 Requerimiento Principal

El sistema debe proveer una **API REST** que permita a un **chatbot de debate** mantener una conversación con el usuario, defendiendo de forma **coherente y persuasiva** una postura sobre un tema, incluso si esta es irracional.  

---

## 🎯 Objetivos clave

1. **Inicio de conversación**
   - Cuando el cliente envía el primer mensaje con `conversation_id = null`, la API debe:
     - Generar un nuevo `conversation_id`.
     - Definir automáticamente un **tema de debate** y una **postura fija** para el chatbot (ejemplo: “La Tierra es plana”).
     - Responder con un mensaje inicial que refleje esa postura.  

2. **Continuidad de la conversación**
   - Cuando el cliente envía mensajes con un `conversation_id` existente:
     - El chatbot debe **mantener la misma postura inicial**.
     - Usar el **historial de los últimos 5 mensajes por cada rol (usuario/bot)** para construir respuestas coherentes.
     - Persuadir al usuario sin cambiar de opinión.

3. **Formato de comunicación**
   - **Entrada (Request JSON):**

     ```json
     {
         "conversation_id": "text" | null,
         "message": "text"
     }
     ```

   - **Salida (Response JSON):**

     ```json
     {
         "conversation_id": "text",
         "message": [
             { "role": "user", "message": "text" },
             { "role": "bot", "message": "text" }
         ]
     }
     ```

   - La respuesta debe contener siempre los últimos **5 pares de mensajes** (máx. historial).  

4. **Consistencia argumentativa**
   - El chatbot debe:
     - Sostener la postura inicial **sin contradecirse**.
     - Usar argumentos persuasivos pero no agresivos.
     - Evitar desviarse a otros temas no relacionados.

5. **Restricciones**
   - El tiempo máximo de respuesta de la API es **30 segundos**.
   - La API debe estar lista para manejar múltiples conversaciones en paralelo.
   - El sistema debe poder correr en **Docker** para facilitar despliegue y pruebas.
