"""
Especificación OpenAPI 3.0.3 oficial y viva para 'El Restaurante de Django' (FORMO DEV).
Proporciona documentación interactiva, contratos para Frontend y suite de pruebas para QA.
"""

OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "El Restaurante de Django API • FORMO DEV",
        "version": "5.1.0",
        "description": (
            "API RESTful y Documentación Viva de **El Restaurante de Django**.\n\n"
            "Diseñada para pruebas de **QA**, integración de **Frontend**, "
            "y sincronización en tiempo real del sistema gastronómico formoseño.\n\n"
            "### Capacidades Clave:\n"
            "- 🍽️ **Comandas & Pedidos:** Flujo completo de pedidos, estados de cocina y auditoría.\n"
            "- 📋 **Menú Típico:** Catálogo de platos y bebidas autóctonas (Surubí, Chipá Guazú, Tereré).\n"
            "- 🧉 **Sensei Formoseño:** Asistente IA para resolver dudas de arquitectura Django, Docker y MVT.\n"
            "- 💻 **Terminal de Desafíos:** Ejecución pedagógica de comandos de consola.\n"
            "- 🌱 **Semillas:** Reinicio rápido de la base de datos para pruebas automatizadas de QA."
        ),
        "contact": {
            "name": "Comunidad FormoDevs",
            "url": "https://github.com/gerardomedina",
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        }
    },
    "servers": [
        {
            "url": "/",
            "description": "Servidor Local / Docker Compose"
        }
    ],
    "tags": [
        {
            "name": "Comandas & Pedidos",
            "description": "Operaciones CRUD para la gestión de comandas del restaurante y tablero Kanban."
        },
        {
            "name": "Catálogo del Menú",
            "description": "Consulta de platos y bebidas típicas disponibles."
        },
        {
            "name": "Asistente Sensei IA",
            "description": "Consultas técnicas al mentor senior de Django, Docker y arquitectura."
        },
        {
            "name": "Laboratorio & Terminal",
            "description": "Evaluador de misiones prácticas y comandos de consola."
        },
        {
            "name": "Mantenimiento & QA",
            "description": "Herramientas de reinicio de base de datos y carga de semillas para testing."
        }
    ],
    "paths": {
        "/api/pedidos/": {
            "get": {
                "tags": ["Comandas & Pedidos"],
                "summary": "Listar todas las comandas",
                "description": "Retorna la lista completa de pedidos clasificados por estado para el tablero en tiempo real.",
                "responses": {
                    "200": {
                        "description": "Lista de pedidos obtenida correctamente.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/PedidosListResponse"
                                },
                                "example": {
                                    "pedidos": [
                                        {
                                            "id": 1,
                                            "cliente_name": "Guillermo (FORMO DEV)",
                                            "mesa": 1,
                                            "plato": "Empanadas Formoseñas",
                                            "plato_icono": "🥟",
                                            "bebida": "Tereré con Menta y Burrito",
                                            "bebida_icono": "🌿",
                                            "notas": "Mucha menta en el tereré, bien helado!",
                                            "estado": "PENDIENTE",
                                            "hora": "19:30"
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            },
            "post": {
                "tags": ["Comandas & Pedidos"],
                "summary": "Crear una nueva comanda (QA / Frontend)",
                "description": "Registra un nuevo pedido en el sistema para una mesa específica.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PedidoCreateInput"
                            },
                            "example": {
                                "cliente_name": "Valeria QA",
                                "mesa": 4,
                                "plato_id": 1,
                                "bebida_id": 5,
                                "notas": "Sin sal agregada, tereré bien frío"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Comanda registrada con éxito.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/PedidoCreateResponse"
                                }
                            }
                        }
                    },
                    "400": {
                        "description": "Datos de entrada inválidos (ej: plato o bebida inexistente)."
                    }
                }
            }
        },
        "/tomar-pedido/": {
            "post": {
                "tags": ["Comandas & Pedidos"],
                "summary": "Tomar pedido (Form-Data o JSON)",
                "description": "Endpoint compatible con formularios HTML tradicionales y peticiones AJAX.",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/PedidoCreateInput"
                            }
                        },
                        "application/x-www-form-urlencoded": {
                            "schema": {
                                "$ref": "#/components/schemas/PedidoCreateInput"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Pedido creado exitosamente."
                    }
                }
            }
        },
        "/cambiar-estado-pedido/{pedido_id}/": {
            "post": {
                "tags": ["Comandas & Pedidos"],
                "summary": "Avanzar estado de una comanda",
                "description": "Avanza el estado del pedido en la máquina de estados: `PENDIENTE` ➔ `PREPARANDO` ➔ `SERVIDO`.",
                "parameters": [
                    {
                        "name": "pedido_id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico del pedido a actualizar",
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Estado avanzado correctamente.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "pedido_id": 1,
                                    "nuevo_estado": "PREPARANDO",
                                    "nuevo_estado_display": "Preparando en Cocina"
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Pedido no encontrado."
                    }
                }
            }
        },
        "/eliminar-pedido/{pedido_id}/": {
            "post": {
                "tags": ["Comandas & Pedidos"],
                "summary": "Eliminar o archivar una comanda",
                "description": "Elimina definitivamente un pedido del sistema.",
                "parameters": [
                    {
                        "name": "pedido_id",
                        "in": "path",
                        "required": True,
                        "description": "ID numérico del pedido a eliminar",
                        "schema": {
                            "type": "integer",
                            "example": 1
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Pedido eliminado correctamente.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "pedido_id": 1
                                }
                            }
                        }
                    },
                    "404": {
                        "description": "Pedido no encontrado."
                    }
                }
            }
        },
        "/api/menu/": {
            "get": {
                "tags": ["Catálogo del Menú"],
                "summary": "Consultar menú gastronómico",
                "description": "Devuelve la carta completa de platos y bebidas típicas formoseñas con precios y disponibilidades.",
                "responses": {
                    "200": {
                        "description": "Catálogo del menú obtenido exitosamente.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "menu": [
                                        {
                                            "id": 1,
                                            "nombre": "Empanadas Formoseñas",
                                            "tipo": "PLATO",
                                            "precio": "3500.00",
                                            "icono": "🥟",
                                            "descripcion": "Carne tierna cortada a cuchillo con huevo duro..."
                                        },
                                        {
                                            "id": 5,
                                            "nombre": "Tereré de Limón y Pomelo",
                                            "tipo": "BEBIDA",
                                            "precio": "1600.00",
                                            "icono": "🍋",
                                            "descripcion": "Jarra de tereré con hielo frappé y pomelo rosado..."
                                        }
                                    ]
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/chatbot/": {
            "post": {
                "tags": ["Asistente Sensei IA"],
                "summary": "Consultar al Sensei Formoseño",
                "description": "Envía una pregunta técnica sobre Django, Docker, PostgreSQL o arquitectura y recibe la respuesta del mentor.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/ChatbotInput"
                            },
                            "example": {
                                "mensaje": "¿Qué es la arquitectura MVT y por qué Django usa Templates en vez de Views convencionales?"
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Respuesta del Sensei generada con éxito.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/ChatbotResponse"
                                },
                                "example": {
                                    "titulo": "🍽️ Arquitectura MVT y Analogía Gastronómica",
                                    "respuesta": "¡Qué hacés, chamigo! Mirá: en Django el Modelo es la Despensa, la Vista es el Cocinero y el Template es el Mozo...",
                                    "tipo": "mvt"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/terminal/": {
            "post": {
                "tags": ["Laboratorio & Terminal"],
                "summary": "Ejecutar comando en la consola de desafíos",
                "description": "Recibe un comando ingresado por el usuario, valida la misión activa y provee feedback pedagógico del Sensei.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/TerminalInput"
                            },
                            "example": {
                                "comando": "python manage.py makemigrations",
                                "mision_actual": 1
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Comando evaluado y salida generada.",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/TerminalResponse"
                                }
                            }
                        }
                    }
                }
            }
        },
        "/api/seed-rapido/": {
            "post": {
                "tags": ["Mantenimiento & QA"],
                "summary": "Resetear y sembrar datos de prueba",
                "description": "Ejecuta de manera controlada el comando `seed_data` para restaurar el menú y comandas iniciales.",
                "responses": {
                    "200": {
                        "description": "Datos sembrados con éxito.",
                        "content": {
                            "application/json": {
                                "example": {
                                    "success": True,
                                    "message": "¡Menú y comandas de prueba cargados con éxito!"
                                }
                            }
                        }
                    },
                    "500": {
                        "description": "Error al ejecutar el sembrador de datos."
                    }
                }
            }
        },
        "/api/notificar-desafio/": {
            "post": {
                "tags": ["WebSockets & Notificaciones Push"],
                "summary": "Emitir Notificación Push WebSocket del Sensei",
                "description": "Dispara manualmente un evento push WebSocket a todos los navegadores conectados en `/ws/progreso/` con actualización de progreso, estado, frase formoseña y avatar SVG dinámico del Sensei.",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "tipo": {
                                        "type": "string",
                                        "enum": ["desafio_completado", "ejercicio_completo"],
                                        "example": "desafio_completado"
                                    },
                                    "nombre_desafio": {
                                        "type": "string",
                                        "example": "Misión 2: Levantar las Paredes"
                                    },
                                    "progreso": {
                                        "type": "integer",
                                        "example": 50
                                    },
                                    "frase": {
                                        "type": "string",
                                        "example": "¡Metiste pared y revoque fino! Tablas vivas en PostgreSQL."
                                    },
                                    "svg": {
                                        "type": "string",
                                        "example": "/static/images/sensei_aprobando.svg"
                                    }
                                }
                            }
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": "Notificación emitida exitosamente por WebSocket al grupo chat_laboratorio_restaurante."
                    }
                }
            }
        }
    },
    "components": {
        "schemas": {
            "PedidoItem": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "example": 1},
                    "cliente_name": {"type": "string", "example": "Guillermo (FORMO DEV)"},
                    "mesa": {"type": "integer", "example": 1},
                    "plato": {"type": "string", "example": "Empanadas Formoseñas"},
                    "plato_icono": {"type": "string", "example": "🥟"},
                    "bebida": {"type": "string", "example": "Tereré con Menta y Burrito"},
                    "bebida_icono": {"type": "string", "example": "🌿"},
                    "notas": {"type": "string", "example": "Bien helado"},
                    "estado": {
                        "type": "string",
                        "enum": ["PENDIENTE", "PREPARANDO", "SERVIDO"],
                        "example": "PENDIENTE"
                    },
                    "hora": {"type": "string", "example": "19:30"}
                }
            },
            "PedidosListResponse": {
                "type": "object",
                "properties": {
                    "pedidos": {
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/PedidoItem"}
                    }
                }
            },
            "PedidoCreateInput": {
                "type": "object",
                "required": ["cliente_name", "mesa"],
                "properties": {
                    "cliente_name": {
                        "type": "string",
                        "description": "Nombre del cliente o comensal",
                        "example": "Carlos Desarrollador"
                    },
                    "mesa": {
                        "type": "integer",
                        "description": "Número de mesa (1 a 12)",
                        "example": 3
                    },
                    "plato_id": {
                        "type": "integer",
                        "nullable": True,
                        "description": "ID del plato del menú",
                        "example": 1
                    },
                    "bebida_id": {
                        "type": "integer",
                        "nullable": True,
                        "description": "ID de la bebida del menú",
                        "example": 5
                    },
                    "notas": {
                        "type": "string",
                        "description": "Instrucciones especiales para el cocinero",
                        "example": "Sin sal agregada y con hielo"
                    }
                }
            },
            "PedidoCreateResponse": {
                "type": "object",
                "properties": {
                    "success": {"type": "boolean", "example": True},
                    "message": {"type": "string", "example": "¡Comanda para Mesa 3 registrada con éxito!"},
                    "pedido": {"$ref": "#/components/schemas/PedidoItem"}
                }
            },
            "ChatbotInput": {
                "type": "object",
                "required": ["mensaje"],
                "properties": {
                    "mensaje": {
                        "type": "string",
                        "description": "Pregunta o consulta técnica para el Sensei",
                        "example": "¿Por qué usamos PostgreSQL en Docker?"
                    }
                }
            },
            "ChatbotResponse": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "example": "🐳 Docker y PostgreSQL 15"},
                    "respuesta": {"type": "string", "example": "¡Excelente pregunta, chamigo! El aislamiento en contenedores permite..."},
                    "tipo": {"type": "string", "example": "docker"}
                }
            },
            "TerminalInput": {
                "type": "object",
                "required": ["comando"],
                "properties": {
                    "comando": {
                        "type": "string",
                        "example": "python manage.py makemigrations"
                    },
                    "mision_actual": {
                        "type": "integer",
                        "example": 1
                    }
                }
            },
            "TerminalResponse": {
                "type": "object",
                "properties": {
                    "output": {"type": "string", "example": "Migrations for 'restaurante':..."},
                    "mision_completada": {"type": "boolean", "example": True},
                    "siguiente_mision": {"type": "integer", "example": 2},
                    "feedback_sensei": {"type": "string", "example": "¡Impecable, chamigo! Creaste los planos de migración..."}
                }
            }
        }
    }
}
