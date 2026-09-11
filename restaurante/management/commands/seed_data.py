"""
Comando de Django para sembrar datos iniciales típicos formoseños en la base de datos.
Uso: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from restaurante.models import Menu, Pedido

class Command(BaseCommand):
    help = 'Carga el menú típico formoseño y comandas de prueba para el laboratorio FORMO DEV'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("🌱 Iniciando carga de datos gastronómicos formoseños..."))

        # Platos típicos
        platos_data = [
            {
                "nombre": "Empanadas Formoseñas",
                "tipo": "PLATO",
                "precio": 3500.00,
                "icono": "🥟",
                "descripcion": "Carne tierna cortada a cuchillo, huevo duro picado, cebolla de verdeo y especias del litoral."
            },
            {
                "nombre": "Chipá Guazú Tradicional",
                "tipo": "PLATO",
                "precio": 4200.00,
                "icono": "🧀",
                "descripcion": "Pastel salado de choclo fresco rallado a mano, queso criollo abundante y cebolla salteada al horno de barro."
            },
            {
                "nombre": "Surubí a la Parrilla",
                "tipo": "PLATO",
                "precio": 7800.00,
                "icono": "🐟",
                "descripcion": "Filete generoso de surubí fresco del río Paraguay con manteca de finas hierbas y rodajas de limón."
            },
            {
                "nombre": "Sopa Paraguaya Artesanal",
                "tipo": "PLATO",
                "precio": 3800.00,
                "icono": "🥧",
                "descripcion": "Bizcochuelo salado tradicional de harina de maíz, queso paraguay fundido y manteca casera."
            },
            {
                "nombre": "Chivito Formoseño a la Estaca",
                "tipo": "PLATO",
                "precio": 9200.00,
                "icono": "🍖",
                "descripcion": "Chivito criollo asado pacientemente a la estaca con leña de quebracho colorado y sal parrillera."
            },
            {
                "nombre": "Chupín de Pescado de Río al Disco",
                "tipo": "PLATO",
                "precio": 8500.00,
                "icono": "🥘",
                "descripcion": "Filet de surubí y pacú en reducción de salsa de tomates de la huerta, pimientos, papas en rodajas y tostadas al disco."
            },
        ]

        # Bebidas típicas
        bebidas_data = [
            {
                "nombre": "Tereré de Limón y Pomelo",
                "tipo": "BEBIDA",
                "precio": 1600.00,
                "icono": "🍋",
                "descripcion": "Jarra de tereré con hielo frappé, rodajas de limón del patio y pomelo rosado exprimido."
            },
            {
                "nombre": "Tereré con Menta y Burrito",
                "tipo": "BEBIDA",
                "precio": 1500.00,
                "icono": "🌿",
                "descripcion": "Infusión fría bien refrescante con hierbas aromáticas recién cosechadas y yerba canchada."
            },
            {
                "nombre": "Mate Dulce con Naranja",
                "tipo": "BEBIDA",
                "precio": 1400.00,
                "icono": "🧉",
                "descripcion": "Mate cebado con cascaritas de naranja secadas al sol y una pizca de azúcar mascabo."
            },
            {
                "nombre": "Paso de los Toros Pomelo",
                "tipo": "BEBIDA",
                "precio": 1800.00,
                "icono": "🥤",
                "descripcion": "La clásica gaseosa de pomelo bien fría para cortar la sed del calor norteño."
            },
        ]

        # Inserción de Menú
        items_creados = 0
        for item in platos_data + bebidas_data:
            obj, created = Menu.objects.update_or_create(
                nombre=item["nombre"],
                defaults={
                    "tipo": item["tipo"],
                    "precio": item["precio"],
                    "icono": item["icono"],
                    "descripcion": item["descripcion"],
                    "disponible": True,
                }
            )
            if created:
                items_creados += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Menú listo: {Menu.objects.count()} ítems en catálogo ({items_creados} nuevos)."))

        # Pedidos demostrativos iniciales (si no existen)
        if Pedido.objects.count() == 0:
            plato_emp = Menu.objects.filter(nombre="Empanadas Formoseñas").first()
            bebida_terere = Menu.objects.filter(nombre="Tereré con Menta y Burrito").first()

            plato_chipa = Menu.objects.filter(nombre="Chipá Guazú Tradicional").first()
            bebida_paso = Menu.objects.filter(nombre="Paso de los Toros Pomelo").first()

            plato_surubi = Menu.objects.filter(nombre="Surubí a la Parrilla").first()
            bebida_limon = Menu.objects.filter(nombre="Tereré de Limón y Pomelo").first()

            Pedido.objects.create(
                cliente_name="Guillermo (FORMO DEV)",
                mesa=1,
                plato=plato_emp,
                bebida=bebida_terere,
                notas="Mucha menta en el tereré, bien helado chamigo!",
                estado="PENDIENTE"
            )

            Pedido.objects.create(
                cliente_name="Valeria & Amigos",
                mesa=4,
                plato=plato_chipa,
                bebida=bebida_paso,
                notas="Poco picante, por favor",
                estado="PREPARANDO"
            )

            Pedido.objects.create(
                cliente_name="Marcos Desarrollador",
                mesa=7,
                plato=plato_surubi,
                bebida=bebida_limon,
                notas="Al punto con bastante limón",
                estado="SERVIDO"
            )

            self.stdout.write(self.style.SUCCESS("✅ 3 Pedidos de prueba creados en estados PENDIENTE, PREPARANDO y SERVIDO."))
        else:
            self.stdout.write(self.style.NOTICE(f"ℹ️ Ya existían {Pedido.objects.count()} pedidos en la comanda."))

        self.stdout.write(self.style.SUCCESS("🎉 ¡Carga inicial completada con éxito para FORMO DEV!"))
