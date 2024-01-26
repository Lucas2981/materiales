from django.contrib import admin
from .models import Obra, sector, material, IniciarPedidoSector


class IniciarPedidoSectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'user','created','validated') #lo que se muestra en la lista
    search_fields = ('name__name','user__username','user__groups__name', 'sector__name') #campos para buscar
    list_filter = ('name__name', 'sector') #filtros
    def user_group(self, obj):
        return ' - '.join([t.name for t in obj.user.groups.all().order_by('name')])
    user_group.short_description = 'Grupo'
admin.site.register(IniciarPedidoSector,IniciarPedidoSectorAdmin)


admin.site.register(Obra)
admin.site.register(sector)
admin.site.register(material)

