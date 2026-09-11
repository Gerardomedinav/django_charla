from django.db import models

class Menu(models.Model):
    TIPO_CHOICES = [
        ('PLATO', 'Plato Principal'),
        ('BEBIDA', 'Bebida'),
    ]

    nombre = models.CharField(max_length=120, verbose_name="Nombre del ítem")
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='PLATO', verbose_name="Tipo")
    precio = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, verbose_name="Precio ($)")
    descripcion = models.TextField(blank=True, verbose_name="Descripción gastronómica")
    icono = models.CharField(max_length=20, default='🍽️', verbose_name="Emoji o Ícono")
    disponible = models.BooleanField(default=True, verbose_name="¿Disponible?")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ítem de Menú"
        verbose_name_plural = "Ítems del Menú"
        ordering = ['tipo', 'nombre']

    def __str__(self):
        return f"{self.icono} {self.nombre} - ${self.precio}"


class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente (En Espera)'),
        ('PREPARANDO', 'En el Fuego (Cocina)'),
        ('SERVIDO', 'Servido a la Mesa'),
    ]

    cliente_name = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    mesa = models.PositiveSmallIntegerField(default=1, verbose_name="Número de Mesa")
    plato = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_plato',
        limit_choices_to={'tipo': 'PLATO'},
        verbose_name="Plato Típico"
    )
    bebida = models.ForeignKey(
        Menu,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pedidos_bebida',
        limit_choices_to={'tipo': 'BEBIDA'},
        verbose_name="Bebida Típica"
    )
    notas = models.CharField(max_length=255, blank=True, default='', verbose_name="Notas del Mozo")
    estado = models.CharField(
        max_length=15,
        choices=ESTADO_CHOICES,
        default='PENDIENTE',
        verbose_name="Estado de la Orden"
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Hora del Pedido")
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pedido de la Casa"
        verbose_name_plural = "Pedidos de la Casa"
        ordering = ['-creado_en']

    def __str__(self):
        return f"Mesa {self.mesa} - {self.cliente_name} ({self.get_estado_display()})"

    def avanzar_estado(self):
        """Avanza el estado del pedido en el flujo de cocina: PENDIENTE -> PREPARANDO -> SERVIDO"""
        if self.estado == 'PENDIENTE':
            self.estado = 'PREPARANDO'
        elif self.estado == 'PREPARANDO':
            self.estado = 'SERVIDO'
        self.save()
        return self.estado
