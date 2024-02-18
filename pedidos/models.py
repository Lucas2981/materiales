from django.db import models
from django.contrib.auth.models import User
# from django.contrib.gis.db import models


class Obra(models.Model):
    areas_SOP = (('0','Escolar'),('1','Infraestructura'),('2','Intendencia'),('3','Salud'))
    name = models.CharField(max_length=200, verbose_name='Obra')
    location = models.CharField(max_length=200, verbose_name='Ubicación', blank=True, null=True)
    area = models.CharField('Area',max_length=1,choices=areas_SOP)
    dpto = models.CharField(max_length=150, blank=True, null=True, verbose_name='Departamento')
    localidad = models.CharField(max_length=150, blank=True, null=True, verbose_name='Localidad')
    municipio = models.CharField(max_length=150, blank=True, null=True, verbose_name='Municipio')
    frac = models.CharField(max_length=2, blank=True, null=True, verbose_name='Fracción')
    radio = models.CharField(max_length=2, blank=True, null=True, verbose_name='Radio')
    tipo = models.CharField(max_length=150, blank=True, null=True, verbose_name='Tipo')
    internacion = models.CharField(max_length=150, blank=True, null=True, verbose_name='Internación')
    nivel_sector = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nivel/Sector')
    plaza = models.IntegerField(blank=True, null=True, verbose_name='Plaza')
    lugar = models.CharField(max_length=150, blank=True, null=True, verbose_name='Lugar')
    cue = models.IntegerField(blank=True, null=True, verbose_name='CUE')
    anexo = models.CharField(max_length=2, blank=True, null=True, verbose_name='Anexo')
    cp = models.CharField(max_length=5, blank=True, null=True, verbose_name='CP')
    periodo_func = models.CharField(max_length=150, blank=True, null=True, verbose_name='Periodo de Funcionamiento')
    geometry = models.CharField(max_length=150, blank=True, null=True, verbose_name='Georeferencia')
    class Meta:
        verbose_name = 'obra'
        verbose_name_plural = 'obras'
        ordering = ['name']
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
class Material(models.Model): 
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
    a_proveedor = models.BooleanField(default=False, verbose_name='A Proveedor')
    orden_compra = models.CharField(max_length=20,unique=True ,blank=True,null=True, verbose_name='Orden de compra')
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
        return f'P{str(self.id)}{user_id} - {self.obra.name}'
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

