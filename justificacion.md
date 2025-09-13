# Estructura del Proyecto – Chat Bot API

Este proyecto fue diseñado siguiendo buenas prácticas de arquitectura en FastAPI y principios de modularidad y escalabilidad. La organización de carpetas busca que el código sea fácil de mantener, extender y probar en el futuro.

## 📂 Estructura General

chatBot/
│
├─ app/                    
│   ├─ main.py              # Punto de entrada principal
│   ├─ models/              # Definición de modelos de datos
│   │   └─ api_models.py    
│   └─ services/            # Lógica de negocio y servicios
│       ├─ debate_service.py
│       └─ response_templates.py
│
├─ tests/                   # Carpeta de pruebas unitarias
│   ├─ test_extract_topic.py
│   ├─ test_limit_history.py
│   └─ test_start_conversation.py
│
├─ Dockerfile               # Configuración para contenerizar la app
├─ config.py                # Configuración del sistema (variables de entorno)
├─ encriptado.py            # Script usado para desencriptado del reto 
├─ Makefile                 # Comandos automáticos para desarrollo y despliegue
├─ requerimiento.md         # Documento de requerimientos iniciales
├─ primer-diagrama.jpg      # Boceto inicial del flujo de conversación
├─ diagrama-funcional.jpg   # Diagrama funcional más detallado
├─ requirements.txt         # Dependencias del proyecto
└─ README.md                # Documentación general del proyecto


# ⚡ Razones de la Estructura

### **Separación de responsabilidades**

main.py solo inicializa la API y define los endpoints.

- La lógica de negocio vive en services/.

- Los modelos de datos se definen en models/.
Esto hace que el proyecto sea modular y fácil de escalar.

- Pruebas unitarias claras
Cada caso de uso (extract_topic, limit_history, start_conversation) tiene su propio archivo de pruebas, facilitando la detección de errores y el mantenimiento continuo.

- Compatibilidad con Docker
Incluir un Dockerfile permite ejecutar la app en cualquier entorno sin problemas de dependencias.

- Automatización con Makefile
El Makefile estandariza comandos frecuentes: instalar, correr pruebas, levantar contenedor, limpiar. Esto agiliza el flujo de desarrollo.

- Documentación visual y escrita
Los diagramas (.jpg) y el documento de requerimientos (.md) ayudan a entender el diseño conceptual y los objetivos iniciales del proyecto.

### **Seguridad y configuración**

config.py maneja variables de entorno (ej. puerto, historial, límites).

.env protege credenciales sensibles.

encriptado.py sirve como base para manejar datos de forma segura.

<br>

## ✅ Beneficios de esta organización

Escalable: se pueden agregar más módulos (ej. auth/, database/) sin romper la estructura.

Legible: cualquier desarrollador nuevo puede ubicar fácilmente cada pieza del sistema.

Portátil: gracias a Docker y requirements.txt, se puede desplegar en local o en la nube.
