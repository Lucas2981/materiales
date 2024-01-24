from django.contrib import admin
from .models import Obra, sector, material, IniciarPedidoSector


admin.site.register(Obra)
admin.site.register(sector)
admin.site.register(material)
admin.site.register(IniciarPedidoSector)

