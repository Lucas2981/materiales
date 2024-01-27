from django.contrib import admin
from .models import Obra, sector, material, IniciarPedidoSector


class IniciarPedidoSectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'sector', 'user','created','validated') #lo que se muestra en la lista
    search_fields = ('name__name','user__username','user__groups__name', 'sector__name') #campos para buscar
    list_filter = ('name__name', 'sector', 'user') #filtros
    def user_group(self, obj):
        return ' - '.join([t.name for t in obj.user.groups.all().order_by('name')])
    user_group.short_description = 'Grupo'
    def save_model(self, request, obj, form, change): # Asignamos el usuario que ha iniciado sesion
        if not obj.user:
            obj.user = request.user
        obj.save()
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Directores').exists():
            return ['name','sector','material','cantidad','description','user','created'] # Solo el campo 'validated' puede ser modificado
        else:
            if obj and obj.validated: # Si el pedido ya ha sido validado no se puede modificar
                return ['name','sector','material','cantidad','description','user','validated','created'] 
            return ['validated','user']  # Si no hay pedidos validados, Los campos 'validated' y 'user' serán de solo lectura
    def get_queryset(self, request):
        '''
        filtramos el queryset para que solo aparezcan las obras del usuario que ha iniciado sesion
        '''
        queryset = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Tecnicos').exists(): 
                queryset = queryset.filter(user=request.user)
                return queryset
            else: 
                return queryset
    def queryset(self, request):
        return super().queryset(request).filter(user__groups__name='Tecnicos').filter(validated=False)


admin.site.register(IniciarPedidoSector,IniciarPedidoSectorAdmin)

class ObraAdmin(admin.ModelAdmin):
    list_display = ('name','user','location', 'contacto','movil')
    search_fields = ('name','user__username','user__groups__name')
    list_filter = ('user__groups','name')
    def user_group(self, obj):
        return ' - '.join([t.name for t in obj.user.groups.all().order_by('name')])
    user_group.short_description = 'Grupo'
admin.site.register(Obra,ObraAdmin)

class materialAdmin(admin.ModelAdmin):
    list_display = ('name','unidad')
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(material,materialAdmin)

admin.site.register(sector)
