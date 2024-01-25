from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Obra(models.Model):
    areas_SOP = (('0','Escolar'),('1','Infraestructura'),('2','Intendencia'),('3','Salud'))
    name = models.CharField(max_length=200, verbose_name='Obra')
    location = models.CharField(max_length=200, verbose_name='Ubicación')
    area = models.CharField('Area',max_length=1,choices=areas_SOP)
    contacto = models.CharField(max_length=100, blank=True)
    movil = models.CharField(max_length=11, blank=True, null=True, verbose_name='Teléfono')
    user= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario')
    def __str__(self):
        return self.name

class sector(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Sector')
    def __str__(self):
        return self.name

class material(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Material')
    unidad = models.CharField(max_length=20, verbose_name='Unidad')
    def __str__(self):
        return self.name

class IniciarPedidoSector(models.Model):
    name=models.ForeignKey(Obra, on_delete=models.CASCADE, verbose_name='Obra')
    sector=models.ForeignKey(sector, on_delete=models.CASCADE, verbose_name='Sector')
    material=models.ForeignKey(material,on_delete=models.CASCADE, verbose_name='Material')
    cantidad=models.CharField(max_length=3, verbose_name='Cantidad')
    user=models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Usuario', editable=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    validated = models.BooleanField(default=False, verbose_name='Aprovado', editable=False)
    
    class Meta:
        verbose_name = 'iniciar pedido'
        verbose_name_plural = 'iniciar pedidos'
        ordering = ['-id']
    def __str__(self):
        return self.name.name
    