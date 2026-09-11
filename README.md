# 🍽️ El Restaurante de Django (Laboratorio Interactivo FORMO DEV)

Bienvenido a **"El Restaurante de Django"**, una aplicación web educativa interactiva desarrollada para la comunidad de **FORMO DEV** (Formosa, Argentina). Este laboratorio enseña de forma visual y práctica la arquitectura **MVT** (Model - View - Template), la ingeniería en **Tres Capas**, y las mejores prácticas de **desarrollo con Docker y PostgreSQL**.

---

## 🌟 1. La Analogía del Restaurante & MVT

Para comprender el flujo de Django, utilizamos la analogía gastronómica:

```text
  [Comensal en la Mesa]
          │  (Petición HTTP a una URL: /tomar-pedido/)
          ▼
   📋 La Carta / Router (config/urls.py & restaurante/urls.py)
          │  (Enruta el pedido al cocinero adecuado)
          ▼
   👨‍🍳 El Cocinero (restaurante/views.py - Capa de Aplicación)
          │  (Consulta insumos vía ORM y aplica la lógica culinaria)
          ▼
   📦 La Despensa (restaurante/models.py & PostgreSQL - Capa de Datos)
          │  (Devuelve los ingredientes / datos consultados)
          ▼
   🤵 El Mozo & El Plato Listo (restaurante/templates/ - Capa de Presentación)
          │  (Renderiza el HTML con Tailwind CSS de vuelta al comensal)
          ▼
  [Comensal Servido - HTTP 200 OK]
```

### Correspondencia Arquitectónica de Tres Capas

| Capa | Rol en el Restaurante | Archivos Django | Tecnologías |
|---|---|---|---|
| **1. Presentación** | El Mozo, la Mesa y el Menú | `templates/dashboard.html`, `urls.py` | HTML5, Tailwind CSS, Vanilla JS |
| **2. Aplicación (Lógica)** | El Cocinero | `views.py`, `chatbot.py` | Python 3.12, Django Views |
| **3. Datos (Persistencia)** | La Despensa e Insumos | `models.py`, `migrations/` | Django ORM, PostgreSQL / SQLite |

---

## 🚀 2. Opciones de Ejecución

### Opción A: Con Docker y Docker Compose (Recomendada)
La forma profesional y reproducible. Levanta en un solo comando el contenedor de la aplicación `web` y la base de datos `PostgreSQL 15` con volumen persistente.

```bash
# 1. Clonar o ingresar al proyecto
cd /home/ger/proyectos/el_restaurante_de_django

# 2. Levantar los contenedores en segundo plano
docker compose up -d

# 3. Cargar datos iniciales (opcional si no se autoejecutaron)
docker compose exec web python manage.py seed_data

# 4. Abrir en tu navegador
# http://localhost:8000
```

Para detener los contenedores:
```bash
docker compose down
```

---

### Opción B: Ejecución Local en Host con Python Virtualenv
Si deseas correrlo directamente en tu máquina con el entorno virtual creado:

```bash
# 1. Activar el entorno virtual
source .venv/bin/activate    # En Linux / WSL
# .venv\Scripts\activate     # En Windows PowerShell

# 2. Instalar dependencias (si aún no lo hiciste)
pip install -r requirements.txt

# 3. Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# 4. Cargar el menú gastronómico formoseño
python manage.py seed_data

# 5. Iniciar el servidor de desarrollo
python manage.py runserver 0.0.0.0:8000
```

---

## 🐧 3. Guía Paso a Paso: Linux vs Windows 11 (WSL 2)

### Para desarrolladores en Linux (Ubuntu / Debian):
```bash
# Instalar utilidades y Docker
sudo apt update && sudo apt install -y python3-venv docker.io docker-compose-plugin

# Agregar tu usuario al grupo docker (opcional para no usar sudo)
sudo usermod -aG docker $USER

# Iniciar proyecto
docker compose up -d
```

### Para desarrolladores en Windows 11:
La mejor práctica profesional recomendada por FORMO DEV es trabajar mediante **WSL 2** (Windows Subsystem for Linux):
1. Abrir PowerShell como Administrador y ejecutar:
   ```powershell
   wsl --install -d Ubuntu
   ```
2. Instalar **Docker Desktop** en Windows y activar la casilla:  
   *Settings ➔ General ➔ "Use the WSL 2 based engine"*.
3. Trabajar desde la terminal de Ubuntu WSL exactamente igual que en Linux nativo.

---

## 🛡️ 4. Los 3 Pilares de la Seguridad en Producción

1. **`SECRET_KEY` confidencial**: Nunca se comparte ni se sube a repositorios públicos. Se mantiene en el archivo `.env`.
2. **`DEBUG = False` en producción**: Evita filtrar código fuente, contraseñas de bases de datos o configuraciones en pantallas de error públicas.
3. **`.env` fuera de Git**: En `.gitignore` se bloquea el archivo `.env` y sólo se comparte `.env.example` con variables de referencia.

---

## 🎮 5. Desafíos Interactivos de Consola

La aplicación incluye una terminal interactiva en el navegador para que los alumnos de FORMO DEV practiquen los 4 comandos esenciales:

1. **Misión 1**: `python manage.py makemigrations` (Genera el plano arquitectónico).
2. **Misión 2**: `python manage.py migrate` (Construye las tablas en la base de datos).
3. **Misión 3**: `docker compose up -d` (Orquesta los contenedores en segundo plano).
4. **Misión 4**: `python manage.py seed_data` (Siembra los platos y bebidas formoseñas).

Comandos auxiliares soportados en la consola: `help`, `status`, `ls`, `clear`, `pwd`, `whoami`.

---

## 🧉 6. El Asistente Virtual: "El Sensei Formoseño"

En la esquina inferior derecha dispones del widget interactivo del **Sensei Formoseño**, un mentor técnico con jerga y calidez local (*"chamigo"*, *"tereré de por medio"*, *"metele ficha"*) que responde preguntas sobre:
- MVT y Arquitectura de 3 Capas.
- El ORM de Django vs sentencias SQL crudo.
- Docker, Compose y persistencia de volúmenes.
- Comparativas: Django vs Laravel (PHP) y Django vs Flask.
- Despliegue en la nube con Microsoft Azure.
- Seguridad y mejores prácticas.

---

## 📂 7. Estructura del Proyecto

```text
el_restaurante_de_django/
├── Dockerfile                  # Receta del contenedor Python 3.12
├── docker-compose.yml          # Orquestación de servicios web y PostgreSQL
├── requirements.txt            # Dependencias del proyecto
├── manage.py                   # CLI administrativo de Django
├── .env                        # Variables de entorno activas
├── .env.example                # Plantilla de variables de entorno
├── .gitignore                  # Exclusiones de control de versiones
├── config/                     # Configuración central del proyecto Django
│   ├── settings.py             # Configuración dual (Postgres en Docker / SQLite en Host)
│   ├── urls.py                 # Enrutador principal
│   ├── wsgi.py                 # Punto de entrada WSGI
│   └── asgi.py                 # Punto de entrada ASGI
└── restaurante/                # Aplicación principal del laboratorio
    ├── models.py               # Modelos Menu y Pedido (Capa de Datos)
    ├── views.py                # Controladores y lógica de comanda (Capa de Aplicación)
    ├── urls.py                 # Rutas de la app restaurante
    ├── chatbot.py              # Motor semántico del Sensei Formoseño
    ├── admin.py                # Registro en el panel de administración
    ├── management/commands/
    │   └── seed_data.py        # Comando de carga gastronómica formoseña
    ├── static/images/          # Ilustraciones SVG vectoriales optimizadas
    │   ├── sensei_avatar.svg   # Avatar del Sensei Formoseño con tereré
    │   ├── mvt_analogia.svg    # Diagrama de Tres Capas y MVT
    │   └── restaurante_hero.svg# Banner nocturno de la Costanera
    └── templates/restaurante/
        └── dashboard.html      # Frontend reactivo con Tailwind CSS
```

---

**Comunidad FORMO DEV**  
*Impulsando el talento tecnológico desde Formosa para el mundo entero.* ☀️🇦🇷
