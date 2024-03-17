from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
token = os.environ.get('API_TOKEN')

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
        verbose_name = 'institución'
        verbose_name_plural = 'Intituciones'
        ordering = ['name']
    def __str__(self):
        return self.name

class Obra2(models.Model):
    name = models.ForeignKey(Obra, on_delete=models.CASCADE, verbose_name='Obra')
    codObra = models.CharField(max_length=200, verbose_name='Cod. Obra', blank=True, null=True)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Inspector')
    inicio = models.DateField(verbose_name='Fecha de inicio')
    plazo = models.IntegerField(verbose_name='Plazo')
    entrega = models.DateField(verbose_name='Fecha de entrega estimada', blank=True, null=True)
    finalizada = models.BooleanField(verbose_name='Finalizada', default=False)
    fecha_finalizada = models.DateField(verbose_name='Fecha de finalización real', blank=True, null=True)
    class Meta:
        verbose_name = 'obra2'
        verbose_name_plural = 'obras2'
        ordering = ['name']
    
    def __str__(self):
        return self.name.name
    
    def save(self, *args, **kwargs):
        self.codObra = f'{str(self.name.name)[:4].upper()}{str(self.id).zfill(4)}{str(self.name.dpto)[:3].upper()}'
        self.entrega = self.inicio + timedelta(days=self.plazo)
        super().save(*args, **kwargs)
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
    problema = models.TextField(max_length=6000, blank=True,null=True,verbose_name='Planteo de problema', help_text='Explicar brevemente el problema que quieres resolver.')
    propuesta = models.TextField(max_length=6000, blank=True,null=True,verbose_name='Propuesta de solución', help_text='Explicar brevemente la solución que quieres implementar.')
    memoria = models.TextField(max_length=3000, blank=True,null=True,verbose_name='Memoria', help_text='Memoria enriquecida sobre el problema', default="")
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
    
    def save(self):
        if self.problema and self.propuesta:
            genai.configure(api_key=token)
            model = genai.GenerativeModel(model_name="gemini-pro")

            consulta = f'''Objetivo: Generar un informe tecnico del rubro de al construcción ordenado sobre una obra específica, incluyendo su nombre, introducción, problema principal, solución planteada,  desarrollo y conclusión final. No superar los 3000 caracteres.

Nombre de la obra: {self.obra.name.title()}
Problema: {self.problema}
Solución planteada: {self.propuesta}

Salida:

Informe:

Nombre de la obra: {self.obra.name.title()}

Introducción:
Contextualización del tema o ámbito en el que se enmarca la obra, presentación del problema principal que aborda la obra, importancia o relevancia del problema.

Problemática:
Descripción detallada del problema, incluyendo causas, consecuencias y posibles impactos. Análisis de las diferentes perspectivas o enfoques sobre el problema. Evidencia o datos que sustentan la problemática. Hasta 500 caracteres

Propuesta de intervención:
Descripción detallada de la solución propuesta para acondicionar la obra, incluyendo fundamentos o argumentos que la sustentan, posibles beneficios o ventajas de la solución y recursos necesarios para su implementación. Hasta 500 caracteres

Conclusión final:
Resumen de los puntos clave del informe. Reflexión sobre la viabilidad y potencial impacto de la solución propuesta. Aporte o valor de la obra para abordar el problema.
'''
            response = model.generate_content(consulta)
            self.memoria = response.text.replace("**", "")
        else:
            self.memoria = ""
        super().save()

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

    