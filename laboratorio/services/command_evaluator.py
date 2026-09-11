"""
Servicio de análisis y clasificación pedagógica de comandos para la terminal interactiva.
Reconoce comandos válidos de Linux, Docker, Docker Compose, Git, Pip y Django/Python.
"""

class CommandEvaluatorService:
    LINUX_COMMANDS = {
        'cat': ("Linux / Bash", "Concatena y muestra el contenido de uno o más archivos de texto en la pantalla."),
        'grep': ("Linux / Bash", "Busca patrones o expresiones regulares dentro de archivos de texto o salidas de comandos."),
        'find': ("Linux / Bash", "Busca archivos y directorios en el sistema según criterios como nombre, tamaño o fecha."),
        'mkdir': ("Linux / Bash", "Crea uno o más directorios o carpetas nuevas en el sistema de archivos."),
        'rm': ("Linux / Bash", "Elimina archivos o directorios de forma permanente (ej: rm -rf carpeta)."),
        'rmdir': ("Linux / Bash", "Elimina directorios vacíos del sistema de archivos."),
        'touch': ("Linux / Bash", "Crea un archivo vacío o actualiza la fecha de modificación de un archivo existente."),
        'cp': ("Linux / Bash", "Copia archivos o directorios desde un origen hacia un destino."),
        'mv': ("Linux / Bash", "Mueve o renombra archivos o carpetas en el sistema de archivos."),
        'echo': ("Linux / Bash", "Imprime una línea de texto o el valor de una variable de entorno en la terminal."),
        'chmod': ("Linux / Bash", "Modifica los permisos de lectura, escritura y ejecución de un archivo (ej: chmod +x manage.py)."),
        'chown': ("Linux / Bash", "Cambia el usuario y grupo propietario de un archivo o carpeta."),
        'sudo': ("Linux / Bash", "Ejecuta un comando con permisos elevados de superusuario (root)."),
        'apt': ("Linux (Debian/Ubuntu)", "Gestor de paquetes avanzado para instalar, actualizar y eliminar software del sistema operativo."),
        'apt-get': ("Linux (Debian/Ubuntu)", "Herramienta clásica de gestión de paquetes para distribuciones Debian/Ubuntu."),
        'systemctl': ("Linux (systemd)", "Controla y administra los servicios del sistema, demonios y estado de arranque."),
        'service': ("Linux / SysV", "Ejecuta comandos de inicio, parada o reinicio sobre servicios del sistema."),
        'htop': ("Linux / Bash", "Monitor interactivo y visual del uso de CPU, memoria RAM y procesos en tiempo real."),
        'top': ("Linux / Bash", "Muestra la lista de procesos activos del sistema y el consumo de recursos de CPU y memoria."),
        'ps': ("Linux / Bash", "Muestra una instantánea de los procesos activos asociados a la sesión o al usuario."),
        'kill': ("Linux / Bash", "Envía una señal de terminación a un proceso en ejecución mediante su PID."),
        'pkill': ("Linux / Bash", "Envía una señal de terminación a procesos coincidentes por nombre."),
        'df': ("Linux / Bash", "Informa el espacio libre y ocupado en los discos rígidos y particiones montadas."),
        'free': ("Linux / Bash", "Muestra la cantidad de memoria RAM y Swap libre, usada y en caché."),
        'uname': ("Linux / Bash", "Muestra información de la arquitectura y la versión del kernel del sistema operativo."),
        'date': ("Linux / Bash", "Muestra o ajusta la fecha y hora del sistema operativo."),
        'history': ("Linux / Bash", "Lista los comandos ejecutados anteriormente en la sesión de la terminal."),
        'export': ("Linux / Bash", "Define o exporta una variable de entorno para que esté disponible en los subprocesos."),
        'env': ("Linux / Bash", "Muestra todas las variables de entorno actualmente configuradas en la sesión."),
        'source': ("Linux / Bash", "Ejecuta los comandos de un script en la shell actual (ej: source .venv/bin/activate)."),
        'curl': ("Linux / Red", "Transfiere datos desde o hacia un servidor mediante protocolos HTTP, HTTPS, FTP, etc."),
        'wget': ("Linux / Red", "Descarga archivos desde la web mediante peticiones HTTP o FTP en segundo plano."),
        'nano': ("Linux / Editor", "Editor de texto ligero y sencillo en la terminal para modificar código o archivos de configuración."),
        'vim': ("Linux / Editor", "Editor de texto modal avanzado y de alta eficiencia en la terminal."),
        'vi': ("Linux / Editor", "El clásico editor de texto visual de los sistemas Unix."),
        'ssh': ("Linux / Red", "Inicia una sesión de terminal remota cifrada y segura en otro servidor."),
        'ping': ("Linux / Red", "Envía paquetes ICMP para verificar si un servidor o IP responde a través de la red."),
        'tar': ("Linux / Archivos", "Empaqueta o descomprime archivos comprimidos (.tar.gz, .tar.bz2)."),
        'zip': ("Linux / Archivos", "Empaqueta archivos en formato comprimido .zip."),
        'unzip': ("Linux / Archivos", "Descomprime archivos con extensión .zip."),
        'which': ("Linux / Bash", "Localiza y muestra la ruta absoluta del archivo ejecutable de un comando en el PATH."),
        'whereis': ("Linux / Bash", "Localiza el binario, el código fuente y la página del manual de un comando."),
        'head': ("Linux / Bash", "Muestra las primeras líneas de un archivo de texto."),
        'tail': ("Linux / Bash", "Muestra las últimas líneas de un archivo (ej: tail -f para monitorear logs)."),
        'cd': ("Linux / Bash", "Cambia el directorio de trabajo actual en el árbol de carpetas."),
    }

    @classmethod
    def obtener_info_comando(cls, cmd_norm: str):
        """
        Analiza si el comando ingresado corresponde a un comando válido de Linux,
        Docker, Docker Compose, Git, Python o Django, y devuelve su categoría y utilidad.
        """
        cmd_lower = cmd_norm.lower().strip()
        tokens = cmd_lower.split()
        if not tokens:
            return None, None

        first = tokens[0]
        first_two = " ".join(tokens[:2]) if len(tokens) >= 2 else first

        # 1. Comandos de Django y Python
        if first in ['python', 'python3', './manage.py']:
            if 'manage.py runserver' in cmd_lower:
                return "Django / Python", "Inicia el servidor web local de desarrollo en http://127.0.0.1:8000/ con recarga en vivo ante cambios de código."
            if 'manage.py createsuperuser' in cmd_lower:
                return "Django / Python", "Crea una cuenta de superusuario con permisos totales para administrar el restaurante desde el panel /admin/."
            if 'manage.py test' in cmd_lower:
                return "Django / Python", "Ejecuta la suite de pruebas unitarias y de integración automatizadas para verificar que nada esté roto."
            if 'manage.py shell' in cmd_lower:
                return "Django / Python", "Abre la consola interactiva de Python con todos los modelos y configuraciones de Django importados listos para consultar."
            if 'manage.py check' in cmd_lower:
                return "Django / Python", "Inspecciona el proyecto completo en busca de errores de configuración, modelos o sintaxis sin alterar la base de datos."
            if 'manage.py sqlmigrate' in cmd_lower:
                return "Django / Python", "Muestra el código SQL crudo que Django ejecutará para una migración específica sin aplicarla aún (auditoría previa de arquitecto)."
            if 'manage.py showmigrations' in cmd_lower:
                return "Django / Python", "Lista todas las aplicaciones del proyecto y el estado de sus migraciones ([X] aplicada, [ ] pendiente)."
            if 'manage.py collectstatic' in cmd_lower:
                return "Django / Python", "Recopila todos los archivos estáticos (CSS, JS, imágenes) en la carpeta STATIC_ROOT para el despliegue en producción."
            if 'manage.py dbshell' in cmd_lower:
                return "Django / Python", "Abre la consola nativa del motor de base de datos configurado (psql en PostgreSQL o sqlite3)."
            if 'manage.py inspectdb' in cmd_lower:
                return "Django / Python", "Realiza ingeniería inversa sobre tablas existentes en la BD y genera los modelos de Django correspondientes."
            if '-m venv' in cmd_lower:
                return "Python Virtualenv", "Crea un entorno virtual aislado (.venv) para instalar librerías sin afectar al sistema operativo host."
            if '--version' in cmd_lower or '-v' in cmd_lower:
                return "Python CLI", "Muestra la versión instalada del intérprete de Python en el sistema (ej: Python 3.12 o 3.13)."
            return "Python", "Ejecuta scripts o módulos del intérprete de Python."

        # 2. Docker Compose
        if first_two in ['docker compose', 'docker-compose']:
            if len(tokens) >= 3:
                sub = tokens[2]
                if sub in ['down']:
                    return "Docker Compose", "Detiene y destruye los contenedores, redes y recursos orquestados por el archivo docker-compose.yml."
                if sub in ['build']:
                    return "Docker Compose", "Reconstruye las imágenes de los servicios definidos en el docker-compose.yml."
                if sub in ['logs']:
                    return "Docker Compose", "Muestra los registros consolidados de stdout/stderr de todos los servicios orquestados en tiempo real."
                if sub in ['ps']:
                    return "Docker Compose", "Lista los contenedores y estados específicos de los servicios orquestados por Compose."
                if sub in ['restart']:
                    return "Docker Compose", "Reinicia todos los servicios del docker-compose.yml."
                if sub in ['stop']:
                    return "Docker Compose", "Pausa temporalmente los contenedores de compose sin destruir la red ni los volúmenes."
                if sub in ['exec']:
                    return "Docker Compose", "Ejecuta un comando dentro de uno de los servicios activos (ej: docker compose exec web bash)."
            return "Docker Compose", "Herramienta de orquestación para definir y ejecutar aplicaciones multi-contenedor reproducibles."

        # 3. Docker nativo
        if first == 'docker':
            if len(tokens) >= 2:
                sub = tokens[1]
                if sub == 'ps':
                    return "Docker", "Lista los contenedores que están corriendo actualmente con sus IDs, imágenes, estados y puertos mapeados."
                if sub in ['images', 'image']:
                    return "Docker", "Muestra todas las imágenes de Docker descargadas o construidas en el almacenamiento local."
                if sub == 'build':
                    return "Docker", "Construye una nueva imagen de contenedor a partir de las instrucciones de un Dockerfile."
                if sub == 'run':
                    return "Docker", "Crea e inicia un nuevo contenedor a partir de una imagen de Docker especificada."
                if sub == 'stop':
                    return "Docker", "Detiene de forma segura uno o más contenedores en ejecución (señal SIGTERM)."
                if sub == 'start':
                    return "Docker", "Inicia uno o más contenedores que se encontraban detenidos."
                if sub == 'restart':
                    return "Docker", "Reinicia uno o más contenedores activos o caídos."
                if sub == 'rm':
                    return "Docker", "Elimina uno o más contenedores detenidos del sistema."
                if sub == 'rmi':
                    return "Docker", "Elimina una o más imágenes de Docker del almacenamiento local."
                if sub == 'logs':
                    return "Docker", "Muestra las trazas de salida estándar de un contenedor para depuración de errores."
                if sub == 'exec':
                    return "Docker", "Ejecuta un comando interactivo dentro de un contenedor en ejecución (ej: docker exec -it id bash)."
                if sub in ['volume', 'volumes']:
                    return "Docker", "Administra o lista los volúmenes de almacenamiento persistente (como postgres_data)."
                if sub in ['network', 'networks']:
                    return "Docker", "Administra o lista las redes virtuales aisladas que comunican contenedores entre sí."
                if sub == 'version':
                    return "Docker", "Muestra la versión del cliente y del daemon de Docker instalados."
            return "Docker", "Plataforma de virtualización a nivel de SO para empaquetar aplicaciones en contenedores reproducibles."

        # 4. Pip
        if first in ['pip', 'pip3']:
            if len(tokens) >= 2:
                sub = tokens[1]
                if sub == 'install':
                    return "Pip (Python)", "Descarga e instala paquetes y librerías desde el repositorio oficial PyPI."
                if sub in ['list', 'freeze']:
                    return "Pip (Python)", "Lista todas las dependencias instaladas en el entorno virtual activo con sus versiones exactas."
                if sub == 'show':
                    return "Pip (Python)", "Muestra los detalles, versión y autor de una biblioteca de Python instalada."
                if sub == 'uninstall':
                    return "Pip (Python)", "Desinstala una biblioteca del entorno virtual."
            return "Pip (Python)", "El administrador oficial de paquetes y librerías de Python."

        # 5. Git
        if first == 'git':
            if len(tokens) >= 2:
                sub = tokens[1]
                if sub == 'status':
                    return "Git", "Muestra el estado del árbol de trabajo: archivos modificados, en staging y no rastreados."
                if sub == 'add':
                    return "Git", "Agrega modificaciones de archivos al área de preparación (staging) para el próximo commit."
                if sub == 'commit':
                    return "Git", "Registra una instantánea permanente (commit) con un mensaje descriptivo en el historial del repositorio."
                if sub == 'push':
                    return "Git", "Sube los commits locales a la rama del repositorio remoto (como GitHub o GitLab)."
                if sub == 'pull':
                    return "Git", "Descarga e integra los últimos cambios del repositorio remoto a la rama local."
                if sub == 'log':
                    return "Git", "Muestra el historial cronológico de commits, autores, fechas y mensajes."
                if sub == 'diff':
                    return "Git", "Muestra las diferencias línea por línea entre el código actual y el último commit."
                if sub == 'branch':
                    return "Git", "Lista, crea o elimina ramas de desarrollo en el repositorio."
                if sub in ['checkout', 'switch']:
                    return "Git", "Cambia de rama de trabajo o restaura archivos a un estado anterior."
                if sub == 'clone':
                    return "Git", "Descarga una copia completa de un repositorio remoto en la máquina local."
                if sub == 'init':
                    return "Git", "Inicializa un repositorio Git nuevo en el directorio actual."
            return "Git", "Sistema de control de versiones distribuido estándar de la industria del software."

        # 6. Comandos nativos de Linux y Bash
        if first in cls.LINUX_COMMANDS:
            return cls.LINUX_COMMANDS[first]

        return None, None
