from django.db import models
from django.contrib.auth.models import User


class Obra(models.Model):
    areas_SOP = (('0','Escolar'),('1','Infraestructura'),('2','Intendencia'),('3','Salud'))
    name = models.CharField(max_length=200, verbose_name='Obra')
    location = models.CharField(max_length=200, verbose_name='Ubicación')
    area = models.CharField('Area',max_length=1,choices=areas_SOP)
    contacto = models.CharField(max_length=100, blank=True)
    movil = models.CharField(max_length=11, blank=True, null=True, verbose_name='Teléfono')
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Tec asignado')
    description = models.TextField(max_length=500, blank=True,null=True, verbose_name='Descripción')
    def __str__(self):
        return self.name

class sector(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Sector')
    class Meta:
        verbose_name = 'sector'
        verbose_name_plural = 'sectores'
        ordering = ['-id']
    def __str__(self):
        return self.name

class material(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Material')
    unidad = models.CharField(max_length=20, verbose_name='Unidad')
    class Meta:
        verbose_name = 'insumo'
        verbose_name_plural = 'insumos'
        ordering = ['-id']
    def __str__(self):
        return self.name

class IniciarPedidoSector(models.Model):
    name=models.ForeignKey(Obra, on_delete=models.CASCADE, verbose_name='Obra')
    sector=models.ForeignKey(sector, on_delete=models.CASCADE, verbose_name='Sector')
    material=models.ForeignKey(material,on_delete=models.CASCADE, verbose_name='Material')
    cantidad=models.CharField(max_length=3, verbose_name='Cantidad')
    description = models.TextField(max_length=500, blank=True,null=True, verbose_name='Memoria')
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tec_solicitante')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    validated = models.BooleanField(default=False, verbose_name='Aprobado')
    
    class Meta:
        verbose_name = 'pedido'
        verbose_name_plural = 'pedidos'
        ordering = ['-id']
    def __str__(self):
        return self.name.name
    