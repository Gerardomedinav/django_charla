"""
Motor de Asistente Virtual: 'El Sensei'
Laboratorio FORMO DEV - El Restaurante de Django

Enfoque:
- Basado estrictamente en la presentación oficial ("Django: De Cero a Profesional // El Viaje del Chef Digital")
  y en la documentación oficial de las tecnologías de nuestra página (Django 5.1, Python 3.12, Docker, PostgreSQL, PythonAnywhere, Swagger UI).
- Sin referencias internas a Hugging Face, RAG ni cómo está construido el chatbot por dentro.
- Tono formoseño urbano: cálido, canchero, con chispa y sutil sarcasmo ante preguntas fuera de tema.
- Respuestas equilibradas: ni muy extensas ni muy cortas (2 a 3 párrafos ágiles).
- Latencia ultra-baja: motor local instantáneo (<10ms) con integración a Google Gemini API para consultas abiertas.
"""

import json
import logging
import os
import re
import urllib.error
import urllib.request
from django.conf import settings

logger = logging.getLogger(__name__)

# ==============================================================================
# PROMPT DE SISTEMA PARA GEMINI API (TONO FORMOSEÑO URBANO Y REGLAS)
# ==============================================================================
SENSEI_SYSTEM_PROMPT = """Eres "El Sensei", el mentor virtual de ingeniería de software del laboratorio "El Restaurante de Django" y de la comunidad tech FORMO DEV en Formosa, Argentina.

TU IDENTIDAD Y TONO:
- Tono formoseño urbano: canchero, cálido, con chispa y un toque sutil de sarcasmo si el usuario te pregunta pavadas, pero sin exagerar como gente de campo adentro ("tono formoseño no muy de campo pero sí de esta zona").
- Usas expresiones naturales de nuestra zona: "¡Qué tal, chamigo!", "mirá che", "pariente", "con un buen tereré en mano", "metele ficha", "no te me duermas con las migraciones".
- Explicas con pedagogía senior, claridad técnica y directo al grano.

LONGITUD Y ESTILO DE RESPUESTA:
- Respuestas equilibradas: NI MUY EXTENSAS NI MUY CORTAS (entre 2 y 3 párrafos ágiles o viñetas claras).
- Enfócate en lo esencial, sin vueltas ni introducciones eternas.

REGLAS ESTRICTAS DE CONTEXTO:
1. Habla ÚNICAMENTE de la página, nuestro laboratorio y su contenido técnico (extraído de la presentación oficial y manuales):
   - Python y su ecosistema backend.
   - Django y la arquitectura MVT (Modelo = Despensa, Vista = Cocinero, Template = Mozo, URLs = Recepción/Carta).
   - Buenas prácticas de modularización (Proyecto vs Apps: core, restaurante, laboratorio, notificaciones).
   - Aislamiento del proyecto: entornos virtuales (.venv), requirements.txt, Docker, Docker Compose y variables de entorno (.env).
   - Despliegue en la nube: PythonAnywhere (PaaS, WSGI, Beginner vs Paid), Docker en Azure y base de datos PostgreSQL.
   - APIs REST y documentación interactiva Swagger UI (/swagger/) y ReDoc (/redoc/).
   - Base de datos relacional, ORM de Django, select_related, DecimalField y migraciones seguras (makemigrations, migrate, sqlmigrate).
   - La gastronomía y entorno del restaurante costanero (Costanera Vuelta Fermosa, Chupín de pescado de río, Chivito criollo a la estaca, Sopa paraguaya tradicional).
   - La Ruta de Misiones Interactivas en la Terminal (Pestaña 'Terminal' / Laboratorio):
     Son 8 desafíos prácticos en la consola simulada de FORMO DEV para dominar Django y Docker:
     • ¿Para qué sirven? Permiten experimentar en vivo los comandos reales de desarrollo y despliegue (gestión de archivos, migraciones, superusuario, contenedores Docker y seed de datos) con feedback pedagógico en vivo y progreso sincronizado, sin riesgo de romper tu máquina.
     • ¿Cómo completarlas? Tipeando cada comando exacto en la consola interactiva:
       1. cd restaurante (Ingreso a la cocina del proyecto).
       2. ls (Inspección de archivos y apps modulares).
       3. python manage.py makemigrations (Generación de los planos de migración en Python).
       4. python manage.py migrate (Construcción de tablas en PostgreSQL).
       5. python manage.py createsuperuser (Creación del Chef Ejecutivo para /admin/).
       6. docker compose up -d (Orquestación de contenedores web y db en segundo plano).
       7. docker ps (Control de salud y puertos de los contenedores).
       8. python manage.py seed_data (Carga del menú formoseño y pedidos de prueba).
     Comandos utilitarios en la terminal: help / ayuda (guía rápida), reset / reiniciar (volver al paso 1), status / misiones (ver progreso), clear (limpiar pantalla), whoami, pwd.
2. NUNCA hables de cómo estás construido internamente como chatbot (no menciones RAG, Hugging Face, vector stores, chunks ni embeddings propios).
3. Si el usuario te pregunta sobre cualquier tema que no tenga que ver con la página (recetas de cocina tradicional, pizza, horóscopos, deportes, política, etc.), responde con sarcasmo formoseño amable haciéndole saber que te está preguntando cualquier pavada y aclarándole:
   "¡Ey, chamigo! Yo solo te puedo ayudar con temas de nuestra página: Python, Django MVT, Docker, las 8 misiones en la terminal, modularización, Swagger, PythonAnywhere, aislamiento del proyecto y las buenas prácticas de nuestro restaurante digital"."""

# ==============================================================================
# BASE DE CONOCIMIENTO CURADA DE LA PRESENTACIÓN & DOCS OFICIALES
# ==============================================================================
PRESENTACION_TOPICOS = [
    {
        "id": "mvt_little_lemon",
        "tema": "Arquitectura MVT & Analogía Little Lemon (Slide 6)",
        "palabras_clave": ["mvt", "analogia", "restaurante", "little lemon", "tres capas", "despensa", "cocinero", "mozo", "carta", "contexto", "diccionario", "render", "request", "response"],
        "titulo": "🍽️ Arquitectura MVT & La Analogía del Restaurante",
        "respuesta": (
            "¡Qué tal, chamigo! Mirá che, en Django no usamos el MVC clásico, sino el mero mero **MVT (Model-View-Template)**, que mapea a la perfección con las Tres Capas del restaurante de Little Lemon:\n\n"
            "• **La Despensa (El Modelo - `models.py`):** Es la Capa de Datos. Guarda los ingredientes en PostgreSQL (platos, bebidas y pedidos) asegurando que no se mezclen los tantos.\n"
            "• **El Cocinero (La Vista - `views.py`):** El cerebro operativo (Capa de Aplicación). Recibe el `HttpRequest`, consulta la despensa con el ORM, aplica la lógica de cocina y arma la bandeja de datos.\n"
            "• **El Mozo (El Template - `dashboard.html`):** Capa de Presentación. Toma la bandeja, que técnicamente es un **Diccionario de Python (`context`)**, y te sirve la mesa impecable con HTML y Tailwind CSS.\n"
            "• **La Carta / Recepción (`urls.py`):** El recepcionista que atiende al comensal en la puerta y manda el pedido a la cocina adecuada.\n\n"
            "¡Metele ficha a esta analogía, pariente, que es la clave para entender cualquier backend en Django!"
        )
    },
    {
        "id": "pythonanywhere",
        "tema": "Despliegue en la Nube con PythonAnywhere (Slide 12)",
        "palabras_clave": ["pythonanywhere", "deploy", "despliegue", "hosting", "nube", "wsgi", "static", "collectstatic", "beginner", "hacker"],
        "titulo": "🚀 Despliegue en la Nube: PythonAnywhere",
        "respuesta": (
            "¡Buenas y santas, chamigo! **PythonAnywhere** es la gloria si querés poner tu proyecto online en cinco minutos sin renegar con servidores Linux dedicados:\n\n"
            "• **¿Por qué rinde tanto?** Es una Plataforma como Servicio (PaaS) pensada 100% para Python. Te da consola Bash en el navegador, base de datos integrada y un subdominio gratuito (`tu_usuario.pythonanywhere.com`).\n"
            "• **Los pasos clave:** Subís tu código desde GitHub, creás el entorno virtual con Python 3.12, configurás el archivo WSGI apuntando a `config.wsgi` y mapeás los archivos estáticos (`STATIC_ROOT`) corriendo `python manage.py collectstatic`.\n\n"
            "Para arrancar o mostrar tu laburo en una entrevista va como piña. Ya si necesitás escalar a nivel enterprise con Docker y PostgreSQL masivo, ahí sí pegamos el salto a Azure o AWS."
        )
    },
    {
        "id": "swagger_apis",
        "tema": "APIs REST, OpenAPI & Swagger UI (Slide 9)",
        "palabras_clave": ["swagger", "api", "apis", "rest", "redoc", "openapi", "spectacular", "drf", "endpoint", "endpoints", "qa"],
        "titulo": "⚡ APIs REST & Swagger UI Interactivo",
        "respuesta": (
            "¡Mirá che, qué temazo! En nuestro laboratorio tenemos conectada la documentación viva en **/swagger/** y **/redoc/** usando `drf-spectacular`:\n\n"
            "• **El Contrato Sagrado:** Swagger UI genera la especificación OpenAPI 3.0 automáticamente. Es el contrato entre el backend de Django y quien arme el frontend (sea en React, Next.js o una app móvil en Flutter).\n"
            "• **Pruebas en Vivo:** Con el botón *'Try it out'* podés probar los endpoints de pedidos (`/api/pedidos/`), el menú y las respuestas JSON sin tener que abrir Postman ni escribir una sola línea de frontend.\n\n"
            "En la pestaña 'Funciones' o en el pie de página tenés el acceso directo para auditar la API en vivo, chamigo."
        )
    },
    {
        "id": "docker_aislamiento",
        "tema": "Docker, PostgreSQL & Aislamiento Enterprise (Slide 13)",
        "palabras_clave": ["docker", "dockerfile", "compose", "docker-compose", "postgres", "postgresql", "contenedor", "contenedores", "volumen", "aislamiento"],
        "titulo": "🐳 Docker & Aislamiento de Infraestructura",
        "respuesta": (
            "¡Se acabó el clásico *'pero en mi máquina andaba'*! Con Docker empaquetamos todo el restaurante para que corra idéntico en Formosa, en Buenos Aires o en un servidor de producción:\n\n"
            "• **`Dockerfile`:** Nuestra receta base que compila Python 3.12 con las librerías nativas de PostgreSQL (`libpq-dev`).\n"
            "• **`docker-compose.yml`:** La orquesta completa. Con un solo comando (`docker compose up -d`) levantás el servicio `web` en el puerto 8000 y el motor `db` (PostgreSQL 15).\n"
            "• **Persistencia con Volúmenes:** Los datos viven en el volumen `postgres_data`. Podés reiniciar o tumbar los contenedores mil veces que tus pedidos y el menú no se pierden nunca.\n\n"
            "Aislamiento puro: tu máquina anfitriona queda limpia y el entorno corre encapsulado al 100%."
        )
    },
    {
        "id": "entornos_virtuales",
        "tema": "Entornos Virtuales & Aislamiento del Proyecto (Slide 4)",
        "palabras_clave": ["entorno", "entornos", "virtual", "venv", ".venv", "virtualenv", "pip", "requirements", "requirements.txt", "aislamiento", "freeze"],
        "titulo": "📦 Entornos Virtuales: Aislamiento desde el Día Cero",
        "respuesta": (
            "¡Atendé bien esto, chamigo, que es el mandamiento número uno del desarrollador de Python!\n\n"
            "• **¿Para qué sirve?** El entorno virtual crea una cajita aislada para el proyecto. Si instalás Django 5.1 acá, no se pelea con el Django 4.2 que tengas en otro proyecto viejo en la misma máquina.\n"
            "• **Comandos clave:**\n"
            "  1. Creación: `python -m venv .venv`\n"
            "  2. Activación en Linux/Mac: `source .venv/bin/activate` (o en Windows PowerShell: `.venv\\Scripts\\Activate.ps1`)\n"
            "  3. Congelado: `pip freeze > requirements.txt` para que cualquiera clone tu repo y corra `pip install -r requirements.txt` sin sorpresas.\n\n"
            "Nunca, pero nunca instales librerías en el Python global del sistema. ¡Aislá siempre con `.venv`!"
        )
    },
    {
        "id": "modularizacion_apps",
        "tema": "Modularización: Proyecto vs Apps (Slide 5)",
        "palabras_clave": ["modularizacion", "modular", "app", "apps", "proyecto", "startapp", "startproject", "arquitectura", "core", "laboratorio", "notificaciones"],
        "titulo": "🏢 Modularización: Proyecto vs Apps en Django",
        "respuesta": (
            "Mirá che, para que no te marees con la estructura: **El Proyecto es el edificio, y las Apps son las habitaciones independientes**:\n\n"
            "• **El Proyecto (`config/`):** Contiene la configuración global (`settings.py`), las rutas maestras (`urls.py`) y la pasarela de servidores (`asgi.py`, `wsgi.py`).\n"
            "• **Nuestras 4 Apps Modulares:**\n"
            "  - `core`: Vistas base y dashboard principal.\n"
            "  - `restaurante`: Menú, pedidos y lógica gastronómica.\n"
            "  - `laboratorio`: La terminal interactiva interactiva y este Sensei.\n"
            "  - `notificaciones`: WebSockets con Channels para el push en tiempo real del salón.\n\n"
            "Cada app tiene su propio `models.py`, `views.py` y `urls.py`. Así el código queda ordenado, desacoplado y fácil de mantener entre varios desarrolladores."
        )
    },
    {
        "id": "orm_consultas",
        "tema": "El ORM de Django & Consultas CRUD sin SQL (Slide 7)",
        "palabras_clave": ["orm", "sql", "crud", "select_related", "decimalfield", "query", "filter", "get", "create", "n+1", "inyeccion"],
        "titulo": "🧠 El ORM de Django: Consultas Seguras y Limpias",
        "respuesta": (
            "¡El ORM es magia pura de Python, chamigo! En lugar de escribir sentencias SQL a mano que después te puedan meter un SQL Injection, le hablás a la base como si fueran objetos de Python:\n\n"
            "• **Consultas optimizadas:** Usamos `Menu.objects.filter(disponible=True)` y para los pedidos metemos `select_related('plato', 'bebida')`. ¿Por qué? Porque hace un solo `SQL JOIN` y evita el temido problema de rendimiento N+1.\n"
            "• **Precisión con `DecimalField`:** Para los precios usamos `DecimalField(max_digits=10, decimal_places=2)`. Jamás uses `FloatField` para plata, porque el redondeo binario te come los centavos.\n\n"
            "El ORM se encarga de traducir todo a PostgreSQL sin que te preocupes por la sintaxis específica del motor."
        )
    },
    {
        "id": "migraciones_bd",
        "tema": "Migraciones & Control de Versiones de Base de Datos (Slide 8)",
        "palabras_clave": ["migracion", "migraciones", "makemigrations", "migrate", "sqlmigrate", "esquema", "tabla", "tablas"],
        "titulo": "📐 Migraciones en Django: Plano vs Obra",
        "respuesta": (
            "Para no marearte nunca más con la base de datos, grabate esta regla bien clarita, pariente:\n\n"
            "1. **`python manage.py makemigrations` = El Plano:** Django mira tus cambios en `models.py` y redacta un archivo en Python dentro de `migrations/`. La base de datos todavía no se enteró de nada; tenés el plano en papel.\n"
            "2. **`python manage.py migrate` = La Construcción:** Django agarra los planos pendientes y los ejecuta en PostgreSQL, levantando tablas y columnas reales.\n"
            "3. **`python manage.py sqlmigrate restaurante 0001` = La Auditoría:** Te muestra el SQL crudo que se va a ejecutar antes de impactar en producción.\n\n"
            "¡No toques los archivos de migración a mano a menos que tengas mucha cancha!"
        )
    },
    {
        "id": "seguridad_django",
        "tema": "Los 3 Pilares de la Seguridad en Django",
        "palabras_clave": ["seguridad", "secret_key", "debug", "env", ".env", "gitignore", "csrf", "produccion"],
        "titulo": "🛡️ Los 3 Pilares de Seguridad en Django",
        "respuesta": (
            "¡Ojo al piojo con esto en producción, chamigo! Si no cuidás estos tres puntos te regalás entero:\n\n"
            "1. **`SECRET_KEY` en el `.env`:** Es la llave maestra con la que Django firma cookies y tokens CSRF. Jamás la subas a GitHub ni a repositorios públicos.\n"
            "2. **`DEBUG = False` en producción:** Con `DEBUG=True`, si explota un error Django le muestra el código fuente, contraseñas y variables de entorno a cualquiera que visite la web.\n"
            "3. **`.env` en el `.gitignore`:** En el repositorio solo se comparte un `.env.example` para que el equipo sepa qué variables hacen falta, pero los secretos se quedan en tu máquina.\n\n"
            "Django ya te protege contra CSRF y SQL Injection de fábrica, pero la configuración la tenés que blindar vos."
        )
    },
    {
        "id": "django_vs_laravel_flask",
        "tema": "Django vs Laravel y Flask: Duelo de Frameworks (Slides 3 y 11)",
        "palabras_clave": ["laravel", "flask", "fastapi", "comparativa", "php", "vs", "framework", "baterias", "batteries"],
        "titulo": "⚔️ Django vs Laravel & Flask: Filosofías Distintas",
        "respuesta": (
            "Mirá che, acá la comparación es clara según lo que necesite tu proyecto:\n\n"
            "• **Django vs Laravel:** Laravel (PHP) usa MVC tradicional con controladores y `php artisan`. Django (Python) usa MVT, su propio ORM fuertemente tipado y te regala el panel de administración (`/admin/`) con tres líneas de código. Para proyectos de datos o backend moderno, Python corre con ventaja.\n"
            "• **Django vs Flask:** Flask es un microframework; viene pelado y vos tenés que buscar auth, ORM y migraciones por tu cuenta. Django viene con **'baterías incluidas'** listo para salir a la cancha desde el minuto uno.\n\n"
            "Si querés velocidad de desarrollo, seguridad y robustez, Django es imbatible."
        )
    },
    {
        "id": "monolito_desacoplado",
        "tema": "Evolución Arquitectónica: Monolito vs Desacoplado (Slide 10)",
        "palabras_clave": ["monolito", "monolitico", "desacoplado", "desacoplada", "react", "next", "flutter", "frontend", "backend"],
        "titulo": "🏗️ Monolito vs Arquitectura Desacoplada",
        "respuesta": (
            "¡Excelente punto arquitectónico, pariente! Ambas opciones son válidas según el tamaño del equipo:\n\n"
            "• **Enfoque Monolítico:** Django maneja todo. El backend procesa los datos y renderiza el HTML con sus plantillas (MVT). Es ultra rápido de desarrollar, no tenés problemas de CORS y desplegás un solo servicio.\n"
            "• **Enfoque Desacoplado:** Django actúa como backend puro exponiendo APIs JSON con Django REST Framework (DRF), mientras que el frontend corre en React, Next.js o una app móvil. Te da total libertad visual pero suma complejidad de despliegue.\n\n"
            "En nuestro laboratorio usamos un monolito enriquecido con JavaScript reactivo y WebSockets, ¡lo mejor de los dos mundos!"
        )
    },
    {
        "id": "formosa_costanera",
        "tema": "El Restaurante de Django & La Costanera Vuelta Fermosa (Slide 14)",
        "palabras_clave": ["formosa", "formodevs", "costanera", "vuelta fermosa", "chupin", "surubi", "pacu", "chivito", "sopa paraguaya", "terere", "rio paraguay"],
        "titulo": "☀️ Identidad Norteña: FormoDevs & La Costanera",
        "respuesta": (
            "¡Qué orgullo, chamigo! Este laboratorio nació en el corazón de **FORMO DEV**, la comunidad tecnológica de Formosa, Argentina.\n\n"
            "Inspirados en la hermosa **Costanera Vuelta Fermosa** a orillas del Río Paraguay, unimos la ingeniería de software con nuestras raíces gastronómicas:\n\n"
            "• **Sabores de nuestra carta:** Chupín de pescado de río al disco (Surubí / Pacú), Chivito criollo a la estaca y la clásica Sopa paraguaya formoseña.\n"
            "• **La filosofía:** Entre tereré y tereré con menta y burrito, demostramos que desde el norte argentino se construye software de primer nivel con estándares mundiales.\n\n"
            "¡Podés marchar tu pedido en la pestaña de Salón y verlo avanzar en vivo en el tablero Kanban!"
        )
    },
    {
        "id": "misiones_terminal",
        "tema": "Ruta de Misiones & Desafíos Interactivos en la Terminal (8 Misiones)",
        "palabras_clave": [
            "mision", "misiones", "desafio", "desafios", "terminal", "consola", "simulador",
            "completar", "completarlas", "completarla", "reto", "retos", "paso", "pasos", "ruta",
            "para que sirve", "para que sirven", "como completar", "laboratorio"
        ],
        "titulo": "💻 Ruta de Misiones: Desafíos en la Terminal",
        "respuesta": (
            "¡Qué temazo, chamigo! En la pestaña **'Terminal'** tenés el simulador interactivo de FORMO DEV con **8 misiones guiadas** para dominar Django y Docker paso a paso:\n\n"
            "• **¿Para qué sirven?** Te permiten experimentar en una consola real los comandos de arquitectura, base de datos y despliegue sin riesgo de romper nada en tu máquina. Cada desafío te brinda feedback pedagógico en tiempo real y hace avanzar la barra de progreso por WebSockets.\n\n"
            "• **¿Cómo completarlas? Tipeás el comando exacto en la consola negra:**\n"
            "  1. `cd restaurante`: Ingresás al directorio de trabajo del restaurante.\n"
            "  2. `ls`: Inspeccionás los archivos (`manage.py`, `Dockerfile`, apps modulares).\n"
            "  3. `python manage.py makemigrations`: Generás el plano arquitectónico en Python a partir de `models.py`.\n"
            "  4. `python manage.py migrate`: Levantás las tablas relacionales en la base PostgreSQL.\n"
            "  5. `python manage.py createsuperuser`: Creás la cuenta de Chef Ejecutivo para entrar a `/admin/`.\n"
            "  6. `docker compose up -d`: Levantás los contenedores web y db en segundo plano.\n"
            "  7. `docker ps`: Monitoreás la salud (healthy), uptime y puertos de los contenedores.\n"
            "  8. `python manage.py seed_data`: Cargás el banquete con los platos autóctonos formoseños.\n\n"
            "¡Metele ficha a la terminal, pariente! Si te trabás o querés empezar de nuevo, podés escribir `help` para ver la lista de comandos o `reset` para volver al paso 1."
        )
    },
    {
        "id": "misiones_comandos_utiles",
        "tema": "Comandos Utilitarios de la Terminal (help, reset, status, clear)",
        "palabras_clave": [
            "reset", "reiniciar", "status", "reiniciar misiones", "help", "ayuda", "clear",
            "limpiar consola", "whoami", "pwd"
        ],
        "titulo": "⌨️ Comandos Utilitarios de la Terminal",
        "respuesta": (
            "¡Atendé acá, chamigo! En la consola de la pestaña 'Terminal' tenés varios comandos utilitarios que te salvan las papas:\n\n"
            "• **`help` o `ayuda`:** Te lista en pantalla los 8 desafíos y qué comando espera la consola en cada etapa.\n"
            "• **`status` o `misiones`:** Muestra un reporte en tiempo real de qué pasos tenés completados (✔), cuál te toca resolver ahora (➤) y cuáles están pendientes (⏳).\n"
            "• **`reset` o `reiniciar`:** Restablece todo el laboratorio a la Misión 1 de cero, ideal si querés volver a practicar.\n"
            "• **`clear`:** Limpia el texto de la pantalla para dejar la consola impecable.\n\n"
            "¡Tipealos directamente en el prompt verde de la terminal y probalos vos mismo, che!"
        )
    }
]

# Palabras clave permitidas para el filtro de dominio (Regla 1)
PALABRAS_PERMITIDAS = {
    # Tecnologías de la página
    "django", "python", "mvt", "modelo", "modelos", "vista", "vistas", "template", "templates",
    "orm", "views", "models", "urls", "settings", "contexto", "render", "migrate", "makemigrations",
    "sqlmigrate", "postgres", "postgresql", "docker", "compose", "dockerfile", "api", "apis",
    "backend", "frontend", "rest", "swagger", "redoc", "openapi", "async", "asincronas",
    "pythonanywhere", "deploy", "despliegue", "nube", "cloud", "azure", "wsgi", "asgi",
    "venv", "virtualenv", "entorno", "entornos", "requirements", "pip", "modularizacion",
    "app", "apps", "core", "restaurante", "laboratorio", "notificaciones", "channels", "daphne",
    "decimalfield", "select_related", "crud", "laravel", "flask", "monolito", "desacoplado",
    "secret_key", "debug", ".env", "env", "gitignore", "seguridad", "little lemon", "devatech",
    # Misiones y desafíos de la terminal
    "mision", "misiones", "desafio", "desafios", "terminal", "consola", "bash", "shell",
    "simulador", "reto", "retos", "paso", "pasos", "completar", "completarla", "completarlas",
    "seed_data", "createsuperuser", "superusuario", "reiniciar", "reset", "whoami", "pwd",
    "comando", "comandos",
    # Identidad local
    "formosa", "formodevs", "costanera", "chupin", "surubi", "pacu", "chivito", "sopa paraguaya",
    "terere", "pedido", "pedidos", "kanban", "menu", "carta"
}


# ==============================================================================
# MOTOR DE RESPUESTA LOCAL ULTRA-RÁPIDO (<10 MS)
# ==============================================================================
def normalizar_texto(texto: str) -> str:
    """Normaliza texto a minúsculas y quita acentos para coincidencias semánticas robustas."""
    t = texto.lower()
    t = re.sub(r'[áàäâ]', 'a', t)
    t = re.sub(r'[éèëê]', 'e', t)
    t = re.sub(r'[íìïî]', 'i', t)
    t = re.sub(r'[óòöô]', 'o', t)
    t = re.sub(r'[úùüû]', 'u', t)
    return t


def es_pregunta_fuera_de_tema(mensaje: str) -> bool:
    """Detecta si la pregunta está completamente desconectada de los temas del laboratorio."""
    texto_norm = normalizar_texto(mensaje.strip())

    # Saludos breves o presentaciones se consideran válidos
    if any(s in texto_norm for s in ["hola", "buenas", "que tal", "buen dia", "buenas tardes", "quien sos", "que haces"]):
        if len(texto_norm.split()) <= 4:
            return False

    for palabra in PALABRAS_PERMITIDAS:
        if palabra in texto_norm:
            return False

    return True


def buscar_respuesta_topico_local(mensaje: str) -> dict | None:
    """
    Busca coincidencias directas con los tópicos de la presentación oficial y las misiones.
    Retorna la respuesta curada en menos de 5ms.
    """
    texto = mensaje.lower().strip()
    texto_norm = normalizar_texto(texto)

    # Saludo rápido
    if any(s in texto_norm for s in ["hola", "buenas", "que tal", "buen dia", "buenas tardes"]):
        if len(texto_norm.split()) <= 4:
            return {
                "respuesta": (
                    "¡Qué tal, chamigo! ¿Cómo te va? Acá anda el Sensei con el tereré bien cargado. "
                    "Decime en qué te puedo dar una mano hoy: ¿repasamos la arquitectura MVT, las 8 misiones en la terminal, "
                    "el despliegue en PythonAnywhere, Docker, o cómo modularizar tus apps en Django? ¡Metele ficha!"
                ),
                "titulo": "🧉 ¡Hola, chamigo!",
                "tipo": "saludo"
            }

    # Restricción de tema estricta (Regla 1)
    if es_pregunta_fuera_de_tema(mensaje):
        return {
            "respuesta": (
                "¡Ey, chamigo! ¿A poco me viste cara de chef de restaurante italiano o de Wikipedia? Te me estás yendo por las ramas con esa pregunta.\n\n"
                "Yo solo te puedo ayudar con temas de nuestra página: **Python, Django MVT, Docker, las 8 misiones en la terminal, modularización, Swagger, PythonAnywhere, aislamiento del proyecto y las buenas prácticas de nuestro restaurante digital**.\n\n"
                "Acomodá la bombilla del tereré y preguntame algo de código o de arquitectura, ¡dale que los comensales ya están pidiendo pista!"
            ),
            "titulo": "🛑 Restricción de Tema (Regla 1)",
            "tipo": "offtopic"
        }

    # Detección específica de misiones 1 a 8
    mision_match = re.search(r'\b(?:mision|desafio|paso)\s*([1-8])\b', texto_norm)
    if mision_match:
        num = int(mision_match.group(1))
        info_misiones = {
            1: ("Misión 1: Ingreso al Proyecto", "cd restaurante", "Te sitúa dentro del directorio raíz del restaurante para poder ejecutar `manage.py` y operar con el código."),
            2: ("Misión 2: Inspección de Archivos", "ls", "Lista el contenido del proyecto para verificar que existan `manage.py`, el `Dockerfile` y las apps modulares (`core`, `restaurante`, `laboratorio`)."),
            3: ("Misión 3: El Plano Arquitectónico", "python manage.py makemigrations", "Django inspecciona los cambios en `models.py` y redacta los archivos de migración (el plano técnico en código Python)."),
            4: ("Misión 4: Levantar las Paredes", "python manage.py migrate", "Aplica los planos sobre PostgreSQL, levantando las tablas relacionales para el menú y los pedidos."),
            5: ("Misión 5: Superusuario del Restaurante", "python manage.py createsuperuser", "Crea la cuenta administrativa de Chef Ejecutivo para que puedas entrar con control total al panel de administración en `/admin/`."),
            6: ("Misión 6: Orquestar Contenedores", "docker compose up -d", "Levanta en segundo plano los servicios `web` (Django 5.1) y `db` (PostgreSQL 15) en contenedores totalmente aislados."),
            7: ("Misión 7: Control de Contenedores", "docker ps", "Monitorea la salud (healthy), uptime y mapeo de puertos (`8000:8000`) de los contenedores Docker activos."),
            8: ("Misión 8: El Banquete Formoseño", "python manage.py seed_data", "Ejecuta el script de carga inicial poblando la base con platos autóctonos (Chupín, Chivito, Sopa paraguaya) y pedidos de demostración.")
        }
        if num in info_misiones:
            tit, cmd, desc = info_misiones[num]
            return {
                "respuesta": (
                    f"¡Acá tenés la posta de la **{tit}**, chamigo!\n\n"
                    f"• **¿Para qué sirve?** {desc}\n"
                    f"• **¿Cómo completarla?** Andá a la pestaña **'Terminal'** y tipeá en la consola negra:\n"
                    f"  `{cmd}`\n\n"
                    f"Apenas le des Enter, la consola valida el comando y te habilita el siguiente paso. ¡Metele ficha!"
                ),
                "titulo": f"🎯 {tit}",
                "tipo": "mision_especifica"
            }

    # Búsqueda semántica de tópicos
    mejor_score = 0
    mejor_topico = None

    terminos = set(re.findall(r'\b\w{3,}\b', texto_norm))
    for topico in PRESENTACION_TOPICOS:
        score = 0
        for kw in topico["palabras_clave"]:
            kw_norm = normalizar_texto(kw)
            if kw_norm in texto_norm:
                score += 3
        for t in terminos:
            if t in normalizar_texto(topico["tema"]):
                score += 2
        if score > mejor_score:
            mejor_score = score
            mejor_topico = topico

    if mejor_topico and mejor_score >= 3:
        return {
            "respuesta": mejor_topico["respuesta"],
            "titulo": mejor_topico["titulo"],
            "tipo": "presentacion"
        }

    return None


# ==============================================================================
# LLAMADA A GEMINI API OPTIMIZADA PARA VELOCIDAD (< 2.5 SEG)
# ==============================================================================
def llamar_gemini_rapido(mensaje: str) -> str | None:
    """
    Invoca Gemini API con thinkingBudget=0 y tokens acotados (maxOutputTokens=350)
    para obtener una respuesta precisa y rápida ante preguntas abiertas.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '') or os.environ.get('GEMINI_API_KEY', '')
    model = getattr(settings, 'GEMINI_MODEL', '') or os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash')

    if not api_key:
        return None

    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    payload = {
        "systemInstruction": {
            "parts": [{"text": SENSEI_SYSTEM_PROMPT}]
        },
        "contents": [
            {
                "parts": [{"text": mensaje}]
            }
        ],
        "generationConfig": {
            "temperature": 0.5,
            "maxOutputTokens": 350,
            "thinkingConfig": {
                "thinkingBudget": 0
            }
        }
    }

    try:
        data_bytes = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            endpoint,
            data=data_bytes,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=3.5) as response:
            if response.status == 200:
                res_json = json.loads(response.read().decode('utf-8'))
                candidates = res_json.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts and 'text' in parts[0]:
                        return parts[0]['text'].strip()
    except Exception as e:
        logger.warning(f"Llamada rápida a Gemini omitida ({type(e).__name__}): usando respuesta curada instantánea.")

    return None


# ==============================================================================
# CLASE PRINCIPAL: SENSEIFORMOSENO
# ==============================================================================
class SenseiFormoseno:
    """
    Mentor técnico formoseño:
    - Responde en milisegundos con contenido fiel a la presentación oficial y documentación.
    - Sarcástico y estricto si le preguntan cosas fuera de la página.
    - Sin tecnicismos internos de IA/Hugging Face.
    """

    @classmethod
    def responder(cls, mensaje: str) -> dict:
        """Punto de entrada principal para responder consultas del frontend."""
        if not mensaje or not mensaje.strip():
            return {
                "respuesta": "¡Ey, chamigo! No me dejes la casilla en blanco. Preguntame algo de Django MVT, Docker, modularización o PythonAnywhere.",
                "titulo": "El Sensei",
                "tipo": "saludo"
            }

        # 1. Si está fuera de tema, corte y redirección inmediata con sarcasmo formoseño (<1ms)
        if es_pregunta_fuera_de_tema(mensaje):
            return {
                "respuesta": (
                    "¡Ey, chamigo! ¿A poco me viste cara de cocinero italiano o de Wikipedia? Te me estás yendo por las ramas con esa pregunta.\n\n"
                    "Yo solo te puedo ayudar con temas de nuestra página: **Python, Django MVT, Docker, las 8 misiones en la terminal, modularización, Swagger, PythonAnywhere, aislamiento del proyecto y las buenas prácticas de nuestro restaurante digital**.\n\n"
                    "Acomodá la bombilla del tereré y preguntame algo de código o de arquitectura, ¡dale que los comensales ya están pidiendo pista!"
                ),
                "titulo": "🛑 Restricción de Tema (Regla 1)",
                "tipo": "offtopic"
            }

        # 2. Búsqueda instantánea en los 12 tópicos de la presentación (<5ms)
        respuesta_local = buscar_respuesta_topico_local(mensaje)
        if respuesta_local and respuesta_local["tipo"] != "saludo":
            return respuesta_local

        # 3. Consulta rápida a Gemini API para preguntas abiertas o formulaciones complejas
        respuesta_gemini = llamar_gemini_rapido(mensaje)
        if respuesta_gemini:
            titulo = "🧉 El Sensei"
            tipo = "ai"
            if "pariente" in respuesta_gemini.lower() or "solo te puedo ayudar" in respuesta_gemini.lower():
                titulo = "🛑 Restricción de Tema (Regla 1)"
                tipo = "offtopic"
            elif any(w in respuesta_gemini.lower() for w in ["mvt", "django", "vista", "modelo"]):
                titulo = "🍽️ Sensei: Django MVT"
            elif any(w in respuesta_gemini.lower() for w in ["pythonanywhere", "deploy", "despliegue"]):
                titulo = "🚀 Sensei: PythonAnywhere"
            elif any(w in respuesta_gemini.lower() for w in ["docker", "postgres", "contenedor"]):
                titulo = "🐳 Sensei: Docker & Infraestructura"

            return {
                "respuesta": respuesta_gemini,
                "titulo": titulo,
                "tipo": tipo
            }

        # 4. En caso de timeout de Gemini, fallback inmediato al mejor tópico local
        if respuesta_local:
            return respuesta_local

        # 5. Fallback por defecto formoseño
        return {
            "respuesta": (
                "¡Linda consulta, chamigo! Para no errarle en la arquitectura, acordate de los pilares de nuestra presentación:\n\n"
                "• **El MVT y las Tres Capas:** Despensa (`models.py`), Cocinero (`views.py`) y Mozo (`dashboard.html`).\n"
                "• **Aislamiento:** Siempre `.venv` y Docker para que no se peleen las librerías.\n"
                "• **Despliegue ágil:** PythonAnywhere para salir a la cancha rápido y Swagger para documentar los endpoints.\n\n"
                "¿Querés que profundicemos en alguno de estos puntos, pariente?"
            ),
            "titulo": "💡 Consejo del Sensei",
            "tipo": "default"
        }
