# AGENTS.md — Memoria y Contexto de Ingeniería para Agentes de IA
# Proyecto: El Restaurante de Django (Laboratorio Interactivo FORMO DEV)

Este documento es la **fuente de verdad y memoria técnica canónica** para cualquier agente de IA (Antigravity, Copilot, Cursor, Claude, etc.) que trabaje en este repositorio. Léelo primero para obtener un modelo mental completo del proyecto sin necesidad de explorar todos los archivos del árbol.

---

## 1. Identidad y Misión del Proyecto

- **Nombre Oficial:** El Restaurante de Django (Laboratorio Interactivo FORMO DEV).
- **Propietario / Autor:** Gerardo Medina ([@Gerardomedinav](https://github.com/Gerardomedinav) • `gerardomedinav@hotmail.es`).
- **Repositorio Oficial:** `git@github.com:Gerardomedinav/django_charla.git` / `https://github.com/Gerardomedinav/django_charla`.
- **Propósito:** Plataforma web educativa interactiva desarrollada para la comunidad tecnológica de **FORMO DEV** en Formosa, Argentina. Enseña de manera práctica la arquitectura **MVT** (Model - View - Template), la analogía de las Tres Capas (*Little Lemon*), despliegue en la nube (**PythonAnywhere**), orquestación con **Docker & PostgreSQL**, y APIs interactivas con **Swagger UI / ReDoc**.
- **Estética Visual:** **Cyberpunk HUD ("Neo-Formosa 2088")**.
  - Tipografías: `Orbitron` (titulares HUD), `Share Tech Mono` (telemetría y chips), `JetBrains Mono` (código y consolas).
  - Geometría: Cortes biselados `cyber-chamfer` (en lugar de bordes redondeados tradicionales).
  - Paleta: Fondo ultra-oscuro `#0a0a0f`, Verde Matrix `#00ff88`, Cian Cuántico `#00d4ff`, Ámbar `#ffaa00`, Magenta `#ff00ff`.

---

## 2. Pila Tecnológica (Tech Stack)

| Componente | Tecnología | Rol / Ubicación |
|---|---|---|
| **Backend Framework** | Django 5.1 | Arquitectura MVT, ORM y gestión de apps modulares |
| **Lenguaje** | Python 3.12 | Lógica de negocio, servicios y evaluador de consola |
| **Servidor ASGI/WSGI** | Daphne / Gunicorn | WebSockets en desarrollo/laboratorio y WSGI para despliegue |
| **Bases de Datos** | PostgreSQL 15 & SQLite 3 | Conexión dual inteligente: Postgres en Docker, SQLite en local/PythonAnywhere |
| **Contenedores** | Docker & Docker Compose | Aislamiento enterprise (`web` en puerto 8000, `db` en 5432) |
| **APIs & Docs** | OpenAPI 3.0 / Swagger UI / ReDoc | Documentación interactiva viva en `/swagger/` y `/redoc/` |
| **WebSockets** | Django Channels 4.0 | Telemetría en tiempo real (tablero Kanban y terminal) |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JS | Sin frameworks pesados (React/Next no requeridos) |
| **Asistente IA** | Motor Semántico Local + Gemini 3.5 Flash | Mentor "El Sensei", latencia sub-milisegundo (< 1 ms) |

---

## 3. Arquitectura Modular (Proyecto vs Apps)

El repositorio respeta la buena práctica de Django donde **el Proyecto es el edificio central y las Apps son las habitaciones independientes**:

```text
el_restaurante_de_django/
├── config/                     # PROYECTO: Configuración Maestra
│   ├── settings.py             # Configuración dual (Postgres/SQLite), hosts, apps, CSRF
│   ├── urls.py                 # Enrutador principal, Swagger, ReDoc, admin
│   ├── wsgi.py                 # Punto de entrada WSGI (PythonAnywhere / PaaS)
│   └── asgi.py                 # Punto de entrada ASGI (Daphne / WebSockets)
│
├── core/                       # APP: Vistas Base, Dashboard y Documentación OpenAPI
│   ├── openapi.py              # Especificación manual OpenAPI 3.0 limpia
│   ├── views/dashboard_views.py# Renderizado principal con contexto
│   └── views/docs_views.py     # Vistas embebidas para Swagger UI y ReDoc
│
├── restaurante/                # APP: Lógica Gastronómica y Pedidos
│   ├── models.py               # Menu (platos/bebidas) y Pedido (órdenes)
│   ├── views/menu_views.py     # Listado y catálogo de platos
│   ├── views/pedido_views.py   # CRUD y avance de pedidos (Kanban)
│   ├── backends.py             # Autenticación dual (usuario o email)
│   └── management/commands/
│       └── seed_data.py        # Población inicial con gastronomía formoseña
│
├── laboratorio/                # APP: Simulador de Terminal y Mentor IA
│   ├── services/chatbot_service.py # "El Sensei" Formoseño (motor híbrido y reglas)
│   ├── services/mission_service.py # Evaluador de las 8 misiones interactivas
│   ├── services/command_evaluator.py # Intérprete seguro de comandos Bash
│   ├── views/chatbot_views.py  # Endpoint REST POST /api/chatbot/
│   └── views/terminal_views.py # Endpoint REST POST /api/terminal/
│
└── notificaciones/             # APP: Comunicación en Tiempo Real
    ├── consumers.py            # Consumidor asíncrono WebSocket
    ├── routing.py              # Rutas de sockets (ws/pedidos/, ws/terminal/)
    └── services.py             # Emisión de eventos para actualización reactiva
```

---

## 4. La Analogía del Restaurante (Django MVT)

Para cualquier explicación técnica o feature, mantener la correspondencia de Little Lemon:
- **La Carta / Recepción (`urls.py`):** Atiende la petición HTTP entrante y la deriva al área correspondiente.
- **El Cocinero (La Vista - `views/`):** Capa de Aplicación. Procesa la lógica, consulta a la base de datos y arma la bandeja de datos.
- **La Despensa (El Modelo - `models.py` & PostgreSQL):** Capa de Datos. Persiste platos, pedidos y estados.
- **El Mozo (El Template - `dashboard.html`):** Capa de Presentación. Toma la bandeja (el `context` de Python) y sirve la mesa al comensal con HTML/CSS.

---

## 5. Especificaciones Inviolables de "El Sensei" (Chatbot IA)

1. **CERO Referencias Internas:** NUNCA debe hablar de cómo fue construido por dentro. Prohibido mencionar Hugging Face, FAISS, vector stores, RAG, embeddings propios o chunks.
2. **Contexto Estricto de Dominio:** Solo habla de nuestra página y laboratorio:
   - Python y Django MVT.
   - Buenas prácticas de modularización (Proyecto vs Apps).
   - Aislamiento del proyecto (`.venv`, Docker, variables `.env`).
   - Despliegue en **PythonAnywhere** y Docker en Azure.
   - APIs REST, Swagger UI (`/swagger/`) y ReDoc (`/redoc/`).
   - ORM de Django, `select_related`, `DecimalField`, migraciones seguras y seguridad en producción.
   - Las 8 misiones interactivas de la terminal.
   - Gastronomía de la Costanera Vuelta Fermosa (Chupín de pescado, Chivito a la estaca, Sopa paraguaya).
3. **Regla 1 (Guardrail Fuera de Tema):** Ante preguntas desconectadas (recetas de pizza, política, deportes), devuelve una respuesta sarcástica formoseña amable redirigiendo a los temas de la plataforma.
4. **Tono Formoseño Urbano:** Expresiones naturales (*"¡Qué tal, chamigo!"*, *"mirá che"*, *"pariente"*, *"con un buen tereré en mano"*, *"metele ficha"*).
5. **Longitud Equilibrada:** Ni muy extensas ni muy cortas (2 a 3 párrafos ágiles o viñetas claras).
6. **Motor Híbrido:** Resuelve temas troncales en < 1 ms en memoria local (`buscar_respuesta_topico_local`). Si requiere inferencia abierta, recurre a Gemini 3.5 Flash con `thinkingConfig: {"thinkingBudget": 0}` y max 350 tokens.

---

## 6. La Ruta de 8 Misiones en la Terminal

La pestaña **Terminal** del dashboard evalúa secuencialmente 8 desafíos:
1. `cd restaurante`: Ingreso al directorio de trabajo del restaurante.
2. `ls`: Inspección de archivos y módulos MVT (`manage.py`, `Dockerfile`, apps).
3. `python manage.py makemigrations`: Generación del plano arquitectónico en Python.
4. `python manage.py migrate`: Construcción de tablas relacionales en PostgreSQL.
5. `python manage.py createsuperuser`: Creación del Chef Ejecutivo para `/admin/`.
6. `docker compose up -d`: Orquestación de contenedores web y db en segundo plano.
7. `docker ps`: Control de salud (`healthy`), uptime y puertos mapeados.
8. `python manage.py seed_data`: Carga del menú formoseño y pedidos de demostración.

Comandos utilitarios: `help`, `status`, `reset` (vuelve a la Misión 1), `clear`, `whoami`, `pwd`.

---

## 7. Despliegue en PythonAnywhere

- **Configuración WSGI:** Archivo `/var/www/tu_usuario_pythonanywhere_com_wsgi.py` apuntando a `config.wsgi.application`.
- **Base de Datos:** `settings.py` detecta automáticamente si `DB_HOST` es resolvible. En PythonAnywhere gratuito hace fallback automático a `db.sqlite3` sin romper nada.
- **Archivos Estáticos:** `python manage.py collectstatic --noinput` compila en `staticfiles/`. Mapeo web: `/static/` ➔ `/home/tu_usuario/el_restaurante_de_django/staticfiles`.
- **CSRF:** `CSRF_TRUSTED_ORIGINS` incluye `'https://*.pythonanywhere.com'`.

---

## 8. Protocolo de Seguridad & GitHub Push Protection

- **NUNCA** commitear `.env`, `db.sqlite3`, `db.sqlite3-journal`, `staticfiles/` ni `.venv/` (están en `.gitignore`).
- **NUNCA** dejar claves API hardcodeadas como strings en `.py` o `docker-compose.yml`. Las claves van exclusivamente en variables de entorno leídas por `os.environ.get('GEMINI_API_KEY', '')`.
- Autor de Git para todos los commits del repositorio:
  ```bash
  git config --global user.name "Gerardo Medina"
  git config --global user.email "gerardomedinav@hotmail.es"
  ```

---

## 9. Verificación y Suite de Tests

Antes de dar por concluida cualquier modificación, se debe ejecutar la suite de pruebas unitarias e integración de Django:
```bash
docker compose exec -T web python manage.py test restaurante laboratorio
# O en entorno local:
# python manage.py test restaurante laboratorio
```
**Criterio de Aceptación:** Los 15 tests deben pasar con código de salida 0 en < 0.1s.
