"""
Servicio del Laboratorio Interactivo:
Gestiona el estado, progreso, feedback pedagógico y avance en las 4 misiones guiadas de FORMO DEV.
"""

from notificaciones.services import notificar_avance_usuario
from .command_evaluator import CommandEvaluatorService

class MissionService:
    MISIONES_INFO = {
        1: {
            "nombre": "Misión 1: Ingreso al Proyecto",
            "comando": "cd restaurante",
            "comando_alt": ["cd el_restaurante_de_django", "cd restaurant", "cd ~/el_restaurante_de_django", "cd ./restaurante", "cd /home/ger/proyectos/el_restaurante_de_django"],
            "explicacion": "Ingresa al directorio de trabajo del restaurante para poder ejecutar las herramientas y gestionar el código."
        },
        2: {
            "nombre": "Misión 2: Inspección de Archivos",
            "comando": "ls",
            "comando_alt": ["dir", "ls -l", "ls -la", "ls -F", "ls -lh"],
            "explicacion": "Lista los archivos del proyecto para verificar manage.py, Dockerfile y las apps gastronómicas."
        },
        3: {
            "nombre": "Misión 3: El Plano Arquitectónico",
            "comando": "python manage.py makemigrations",
            "comando_alt": ["python3 manage.py makemigrations", "./manage.py makemigrations"],
            "explicacion": "Genera el archivo de migración en Python (el plano) a partir de los cambios en models.py."
        },
        4: {
            "nombre": "Misión 4: Levantar las Paredes",
            "comando": "python manage.py migrate",
            "comando_alt": ["python3 manage.py migrate", "./manage.py migrate"],
            "explicacion": "Ejecuta los planos pendientes sobre la base de datos para crear o alterar las tablas relacionales."
        },
        5: {
            "nombre": "Misión 5: Superusuario del Restaurante",
            "comando": "python manage.py createsuperuser",
            "comando_alt": ["python3 manage.py createsuperuser", "./manage.py createsuperuser"],
            "explicacion": "Crea la cuenta administrativa con credenciales de Chef Ejecutivo para gestionar el menú en Django Admin."
        },
        6: {
            "nombre": "Misión 6: Orquestar Contenedores",
            "comando": "docker compose up -d",
            "comando_alt": ["docker-compose up -d", "docker compose up", "docker-compose up"],
            "explicacion": "Levanta en segundo plano los servicios web (Django) y db (PostgreSQL 15) en contenedores aislados."
        },
        7: {
            "nombre": "Misión 7: Control de Contenedores",
            "comando": "docker ps",
            "comando_alt": ["docker-compose ps", "docker compose ps", "docker container ls"],
            "explicacion": "Verifica el estado de salud (healthy), uptime y mapeo de puertos de los contenedores activos."
        },
        8: {
            "nombre": "Misión 8: El Banquete Formoseño",
            "comando": "python manage.py seed_data",
            "comando_alt": ["python3 manage.py seed_data", "./manage.py seed_data"],
            "explicacion": "Carga el menú autóctono (empanadas formoseñas, surubí, chipá guazú, tereré) y comandas de demostración."
        },
    }

    @classmethod
    def procesar_comando(cls, cmd: str, mision_actual: int = 1) -> dict:
        cmd_lower = cmd.lower().strip()
        cmd_norm = " ".join(cmd.split())
        cmd_norm_lower = " ".join(cmd_lower.split())

        # Comandos auxiliares de shell
        if cmd_norm_lower in ['clear', 'cls']:
            return {
                'action': 'clear',
                'output': '',
                'mision_completada': False,
                'mision_actual': mision_actual,
            }

        if cmd_norm_lower in ['reset', 'reiniciar', 'restart']:
            notificar_avance_usuario(
                "reset",
                nombre_desafio="Reinicio del Laboratorio",
                progreso=0,
                frase="¡Tabula rasa chamigo! Empezamos desde la Misión 1 con tereré fresco.",
                svg="/static/images/sensei_esperando.svg"
            )
            return {
                'action': 'reset',
                'output': (
                    "🔄 [LABORATORIO REINICIADO]\n"
                    "===========================================================\n"
                    "✔ Estado de misiones restablecido al inicio (Misión 1 de 8).\n"
                    "✔ Barra de progreso sincronizada al 0% vía WebSocket.\n"
                    "✔ Sensei en modo expectante con tereré fresco.\n\n"
                    "🎯 Tu primer objetivo es: Misión 1: Ingreso al Proyecto\n"
                    "👉 Tipeá en la consola: cd restaurante"
                ),
                'mision_completada': False,
                'mision_actual': 1,
                'siguiente_mision': 1,
                'feedback_sensei': "¡Listo el tereré nuevo! Arrancamos desde la Misión 1 para seguir practicando.",
            }

        if cmd_norm_lower in ['help', 'ayuda', '?']:
            return {
                'output': (
                    "Comandos de la Ruta de Desafíos FORMO DEV (8 Misiones):\n"
                    "  1. cd restaurante                   (Desafío 1: ingresar a la cocina)\n"
                    "  2. ls                               (Desafío 2: inspeccionar archivos y apps)\n"
                    "  3. python manage.py makemigrations   (Desafío 3: generar los planos MVT)\n"
                    "  4. python manage.py migrate          (Desafío 4: crear tablas en PostgreSQL)\n"
                    "  5. python manage.py createsuperuser  (Desafío 5: crear el Chef Administrador)\n"
                    "  6. docker compose up -d              (Desafío 6: orquestar contenedores)\n"
                    "  7. docker ps                         (Desafío 7: monitorear contenedores activos)\n"
                    "  8. python manage.py seed_data        (Desafío 8: cargar platos y comandas)\n\n"
                    "Comandos utilitarios:\n"
                    "  • reset | reiniciar                 (Reiniciar todos los desafíos)\n"
                    "  • status | misiones                 (Ver el estado de tu progreso)\n"
                    "  • pwd                               (Ver directorio actual)\n"
                    "  • clear                             (Limpiar la consola)\n"
                    "  • whoami                            (Mostrar usuario activo)"
                ),
                'mision_completada': False,
                'mision_actual': mision_actual,
            }

        if cmd_norm_lower in ['pwd']:
            return {
                'output': '/home/ger/proyectos/el_restaurante_de_django' if mision_actual > 1 else '/home/ger',
                'mision_completada': False,
                'mision_actual': mision_actual,
            }

        if cmd_norm_lower in ['whoami']:
            return {
                'output': 'formodev (Chef Desarrollador Senior • Formosa Tech)',
                'mision_completada': False,
                'mision_actual': mision_actual,
            }

        if cmd_norm_lower in ['status', 'misiones']:
            titulos = [
                cls.MISIONES_INFO[i]["nombre"] for i in range(1, 9)
            ]
            estado_str = "\n".join([
                f"  [{'✔ COMPLETADO' if i + 1 < mision_actual else ('➤ EN CURSO' if i + 1 == mision_actual else '⏳ PENDIENTE')}] {tit}"
                for i, tit in enumerate(titulos)
            ])
            return {
                'output': f"=== ESTADO DEL LABORATORIO FORMO DEV (8 PASOS) ===\n{estado_str}",
                'mision_completada': False,
                'mision_actual': mision_actual,
            }

        mision_completada = False
        siguiente_mision = mision_actual
        feedback_sensei = ""
        output = ""

        # Misión 1: cd restaurante
        if mision_actual == 1:
            if cmd_norm in [cls.MISIONES_INFO[1]["comando"]] + cls.MISIONES_INFO[1]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 2
                output = (
                    "~/el_restaurante_de_django$ pwd\n"
                    "/home/ger/proyectos/el_restaurante_de_django\n"
                    "[DIRECTORIO ACTUALIZADO] Acceso confirmado al entorno del restaurante.\n"
                    "✔ Directorio de trabajo establecido en la raíz del proyecto."
                )
                feedback_sensei = (
                    "¡Bienvenido a la cocina, chamigo! Ya estamos parados en el directorio del restaurante. "
                    "Para la **Misión 2**, inspeccionemos los ingredientes y carpetas con `ls`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 1: Ingreso al Proyecto",
                    progreso=12,
                    frase="¡Adentro de la cocina chamigo! Listos para arrancar.",
                    svg="/static/images/sensei_esperando.svg"
                )

        # Misión 2: ls
        elif mision_actual == 2:
            if cmd_norm in [cls.MISIONES_INFO[2]["comando"]] + cls.MISIONES_INFO[2]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 3
                output = (
                    "Dockerfile  docker-compose.yml  manage.py  requirements.txt  db.sqlite3\n"
                    "config/     core/               restaurante/      laboratorio/   notificaciones/\n"
                    "[SUCCESS] 10 elementos encontrados. Estructura modular MVT y orquestación lista."
                )
                feedback_sensei = (
                    "¡Excelente inspección! Tenés manage.py, la despensa y los módulos listos. "
                    "Ahora en la **Misión 3** preparemos los planos de datos con `python manage.py makemigrations`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 2: Inspección de Archivos",
                    progreso=25,
                    frase="¡Despensa y ficheros a la vista! Todo en orden.",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 3: makemigrations
        elif mision_actual == 3:
            if cmd_norm in [cls.MISIONES_INFO[3]["comando"]] + cls.MISIONES_INFO[3]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 4
                output = (
                    "Migrations for 'restaurante':\n"
                    "  restaurante/migrations/0001_initial.py\n"
                    "    - Create model Menu\n"
                    "    - Create model Pedido\n"
                    "\n[SUCCESS] Archivo de migración 0001_initial.py creado exitosamente."
                )
                feedback_sensei = (
                    "¡Plano arquitectónico listo! Django ya sabe cómo estructurar la carta y las comandas. "
                    "Para la **Misión 4**, levantemos las paredes ejecutando `python manage.py migrate`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 3: El Plano Arquitectónico",
                    progreso=37,
                    frase="¡Plano listo en la mesa del arquitecto! Vamos por las paredes.",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 4: migrate
        elif mision_actual == 4:
            if cmd_norm in [cls.MISIONES_INFO[4]["comando"]] + cls.MISIONES_INFO[4]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 5
                output = (
                    "Operations to perform:\n"
                    "  Apply all migrations: admin, auth, contenttypes, restaurante, sessions\n"
                    "Running migrations:\n"
                    "  Applying contenttypes.0001_initial... OK\n"
                    "  Applying auth.0001_initial... OK\n"
                    "  Applying restaurante.0001_initial... OK\n"
                    "  Applying sessions.0001_initial... OK\n"
                    "\n[SUCCESS] Tablas 'restaurante_menu' y 'restaurante_pedido' creadas en PostgreSQL."
                )
                feedback_sensei = (
                    "¡Paredes firmes y revoque fino! Las tablas ya están vivas en la base de datos. "
                    "En la **Misión 5**, necesitamos crear al Chef Administrador con `python manage.py createsuperuser`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 4: Levantar las Paredes",
                    progreso=50,
                    frase="¡Paredes levantadas en PostgreSQL! Mitad del camino listo.",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 5: createsuperuser
        elif mision_actual == 5:
            if cmd_norm in [cls.MISIONES_INFO[5]["comando"]] + cls.MISIONES_INFO[5]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 6
                output = (
                    "Username: admin_chef\n"
                    "Email address: chef@formodev.org\n"
                    "Password: **********\n"
                    "Password (again): **********\n"
                    "Superuser created successfully.\n"
                    "[AUTH OK] Chef Ejecutivo 'admin_chef' registrado con acceso total a /admin/."
                )
                feedback_sensei = (
                    "¡Chef con delantal y llaves del restaurante! "
                    "Para la **Misión 6**, aislemos los servicios en contenedores con `docker compose up -d`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 5: Superusuario del Restaurante",
                    progreso=62,
                    frase="¡Chef registrado con acceso al panel de administración!",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 6: docker compose up -d
        elif mision_actual == 6:
            if cmd_norm in [cls.MISIONES_INFO[6]["comando"]] + cls.MISIONES_INFO[6]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 7
                output = (
                    "[+] Running 3/3\n"
                    " ✔ Network restaurante_default      Created\n"
                    " ✔ Container restaurante_postgres    Healthy (Port 5432)\n"
                    " ✔ Container restaurante_web         Started (Port 8000 -> 8000)\n"
                    "\n[DOCKER SUCCESS] Servicios activos en segundo plano con volumen 'postgres_data'."
                )
                feedback_sensei = (
                    "¡Qué orquesta, mi viejo! PostgreSQL y Django corriendo reproducibles y aislados. "
                    "En la **Misión 7**, verifiquemos los puertos y contenedores con `docker ps`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 6: Orquestar Contenedores",
                    progreso=75,
                    frase="¡Docker y Postgres orquestados a la perfección!",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 7: docker ps
        elif mision_actual == 7:
            if cmd_norm in [cls.MISIONES_INFO[7]["comando"]] + cls.MISIONES_INFO[7]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 8
                output = (
                    "CONTAINER ID   IMAGE                           STATUS                 PORTS\n"
                    "1c8b99856d63   el_restaurante_de_django-web    Up 2 hours             0.0.0.0:8000->8000/tcp\n"
                    "ee45d03599e1   postgres:15-alpine              Up 2 hours (healthy)   0.0.0.0:5432->5432/tcp\n"
                    "[HEALTHCHECK OK] Todos los contenedores operando sanos y escuchando peticiones."
                )
                feedback_sensei = (
                    "¡Servicios saludables y listos para recibir comensales! "
                    "Llegamos a la **Misión Final (8)**: carguemos el gran menú formoseño con `python manage.py seed_data`."
                )
                notificar_avance_usuario(
                    "desafio_completado",
                    nombre_desafio="Misión 7: Control de Contenedores",
                    progreso=88,
                    frase="¡Monitoreo saludable! Todo listo para el gran banquete final.",
                    svg="/static/images/sensei_aprobando.svg"
                )

        # Misión 8: seed_data (Final)
        elif mision_actual == 8:
            if cmd_norm in [cls.MISIONES_INFO[8]["comando"]] + cls.MISIONES_INFO[8]["comando_alt"]:
                mision_completada = True
                siguiente_mision = 9
                output = (
                    "🌱 Sembrando datos gastronómicos formoseños...\n"
                    "✅ Menú listo: 8 ítems en catálogo (Empanadas Formoseñas, Chipá Guazú, Surubí, Tereré con Menta, etc.).\n"
                    "✅ 3 Pedidos iniciales creados en tiempo real.\n"
                    "🎉 [MISIÓN 8 CUMPLIDA] ¡El Restaurante de Django está 100% operativo!"
                )
                feedback_sensei = (
                    "¡FELICITACIONES, MAESTRO DIGITAL! 🎉🏆 Completaste con éxito los 8 desafíos del laboratorio. "
                    "Has dominado la navegación, migraciones MVT, superusuario, orquestación Docker y siembra de datos."
                )
                notificar_avance_usuario(
                    "ejercicio_completo",
                    nombre_desafio="Misión 8: El Banquete Formoseño",
                    progreso=100,
                    frase="¡Artesanal, con sapucay y orgullo formoseño!",
                    svg="/static/images/sensei_triunfando.svg"
                )

        elif mision_actual >= 9:
            categoria, explicacion = CommandEvaluatorService.obtener_info_comando(cmd_norm)
            if explicacion:
                output = (
                    f"ℹ️ [{categoria}]: '{cmd_norm}'\n"
                    f"• ¿Para qué sirve? {explicacion}\n\n"
                    f"🎉 ¡Ya completaste los 8 desafíos del laboratorio! Podés seguir explorando libremente."
                )
            else:
                output = f"Comando '{cmd}' ejecutado en modo libre. (Escribí 'help' para ver más opciones)."

        # Si NO completó la misión activa
        if not mision_completada and mision_actual < 9:
            comando_otra_mision = None
            for m_num, m_data in cls.MISIONES_INFO.items():
                if m_num != mision_actual and (cmd_norm in [m_data["comando"]] + m_data["comando_alt"]):
                    comando_otra_mision = (m_num, m_data)
                    break

            if comando_otra_mision:
                m_num, m_data = comando_otra_mision
                output = (
                    f"💡 [COMANDO VÁLIDO DE OTRA MISIÓN]: '{cmd_norm}'\n"
                    f"• ¿Para qué sirve? Pertenece a la {m_data['nombre']} ({m_data['explicacion']}).\n\n"
                    f"⚠️ CONSIGNAS DEL LABORATORIO:\n"
                    f"Estás en la Misión {mision_actual} ({cls.MISIONES_INFO[mision_actual]['nombre']}).\n"
                    f"Todavía no es la consigna en este momento; cada paso debe seguir su orden lógico.\n\n"
                    f"🎯 Tu objetivo activo es: {cls.MISIONES_INFO[mision_actual]['nombre']}\n"
                    f"👉 Escribí exactamente: {cls.MISIONES_INFO[mision_actual]['comando']}"
                )
            else:
                categoria, explicacion = CommandEvaluatorService.obtener_info_comando(cmd_norm)
                if explicacion:
                    output = (
                        f"💡 [COMANDO VÁLIDO RECONOCIDO]: '{cmd_norm}' ({categoria})\n"
                        f"• ¿Para qué sirve? {explicacion}\n\n"
                        f"⚠️ CONSIGNAS DEL LABORATORIO:\n"
                        f"Este comando es 100% válido en un entorno profesional de {categoria},\n"
                        f"pero NO es la consigna de la Misión {mision_actual} en este momento.\n\n"
                        f"🎯 Tu objetivo activo es: {cls.MISIONES_INFO[mision_actual]['nombre']}\n"
                        f"👉 Escribí exactamente: {cls.MISIONES_INFO[mision_actual]['comando']}"
                    )
                else:
                    output = (
                        f"Comando '{cmd}' no reconocido en el entorno de pruebas.\n"
                        f"💡 Escribí 'help' para ver comandos disponibles, o avanzá con la Misión {mision_actual}:\n"
                        f"👉 {cls.MISIONES_INFO[mision_actual]['comando']}"
                    )

        return {
            'output': output,
            'mision_completada': mision_completada,
            'siguiente_mision': siguiente_mision,
            'feedback_sensei': feedback_sensei,
        }
