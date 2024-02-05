from django.db import models
from django.contrib.auth.models import User


class Obra(models.Model):
    areas_SOP = (('0','Escolar'),('1','Infraestructura'),('2','Intendencia'),('3','Salud'))
    name = models.CharField(max_length=200, verbose_name='Obra', unique=True)
    location = models.CharField(max_length=200, verbose_name='Ubicación')
    area = models.CharField('Area',max_length=1,choices=areas_SOP)
    contacto = models.CharField(max_length=100, blank=True)
    movil = models.CharField(max_length=11, blank=True, null=True, verbose_name='Teléfono')
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Tec asignado', blank=True, null=True)
    description = models.TextField(max_length=500, blank=True,null=True, verbose_name='Descripción')
    def __str__(self):
        return self.name

class Sector(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Sector')
    class Meta:
        verbose_name = 'sector'
        verbose_name_plural = 'sectores'
        ordering = ['-id']
    def __str__(self):
        return self.name

class Rubros(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Rubro')
    referencia = models.CharField(max_length=150, blank=True, null=True, verbose_name='Referencia')
    class Meta:
        verbose_name = 'rubro'
        verbose_name_plural = 'rubros'
        ordering = ['name']
    def __str__(self):
        return self.name
class Material(models.Model): # Habilidades
    name = models.CharField(max_length=150, verbose_name='Material', unique=True)
    unidad = models.CharField(max_length=20, verbose_name='Unidad')
    referencia = models.CharField(max_length=150, blank=True, null=True, verbose_name='Referencia')
    rubro = models.ForeignKey(Rubros, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Rubro')
    class Meta:
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        ordering = ['rubro','name']
    def __str__(self):
        return self.name+' - '+self.unidad
class Pedido(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Tec asignado', blank=True, null=True)
    memoria = models.TextField(max_length=500, blank=True,null=True, verbose_name='Memoria', help_text='En este campo, debes explicar brevemente el problema que quieres resolver y la solución que propones con los materiales que solicitas. Usa un lenguaje claro, conciso y preciso para expresar tu idea.')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de solicitud')
    validated = models.BooleanField(default=False, verbose_name='Autorizado')
    materiales = models.ManyToManyField(
        Material,
        through='MaterialesPedido',
        blank=True,
    )
    def codigo_pedido(self):
        user_id = str(self.user)[:4].upper()
        return f'P{str(self.id)}{user_id}'
    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['-id']
    def __str__(self):
        user_id = str(self.user)[:4].upper()
        return f'P{str(self.id)}{user_id} <{self.obra.name}>'
class MaterialesPedido(models.Model): 
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.CASCADE, blank=True, null=True)
    cantidad = models.IntegerField()
    sector = models.ForeignKey(Sector, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'material'
        verbose_name_plural = 'materiales'
        ordering = ['-id']
    def __str__(self):
        return self.pedido.obra.name

