from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Obra(models.Model):
    areas_SOP = (('0','Escolar'),('1','Infraestructura'),('2','Intendencia'),('3','Salud'))
    obra = models.CharField(max_length=200)
    ubicacion = models.CharField(max_length=200)
    area = models.CharField('Area',max_length=1,choices=areas_SOP)
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=11, blank=True)
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.obra

class sector(models.Model):
    sector = models.CharField(max_length=150)
    def __str__(self):
        return self.sector

class material(models.Model):
    material = models.CharField(max_length=150)
    unidad = models.CharField(max_length=20)
    def __str__(self):
        return self.material

class IniciarPedidoSector(models.Model):
    obra=models.ForeignKey(Obra, on_delete=models.CASCADE)
    sector=models.ForeignKey(sector, on_delete=models.PROTECT)
    material=models.ForeignKey(material,on_delete=models.PROTECT)
    cantidad=models.CharField(max_length=3)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.obra.obra+' - '+self.sector.sector