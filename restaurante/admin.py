from django.contrib import admin
from .models import Menu, Pedido

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('icono', 'nombre', 'tipo', 'precio', 'disponible')
    list_filter = ('tipo', 'disponible')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('precio', 'disponible')

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('mesa', 'cliente_name', 'plato', 'bebida', 'estado', 'creado_en')
    list_filter = ('estado', 'creado_en')
    search_fields = ('cliente_name', 'notas')
    list_editable = ('estado',)
