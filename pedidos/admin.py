from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import Obra, Sector, Material, Pedido,MaterialesPedido

class MaterialPedidoInline(admin.TabularInline):
    model = MaterialesPedido
    extra = 1
    autocomplete_fields = ['material']
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.validated:  # condicionamos que solo el campo 'materiales' sea modificado en caso de no estar validado por el director
            return ['material', 'sector', 'cantidad']
        return super().get_readonly_fields(request, obj)    
# class PedidoExport(resources.ModelResource):
#     fields = ('obra','user','created','validated', 'materiales__material','materiales__cantidad')
#     class Meta:
#         model = Pedido
    def has_delete_permission(self, request, obj=None):
        if obj and obj.validated:
            return False
        return super().has_delete_permission(request, obj)

class PedidoAdmin(admin.ModelAdmin):
    # resource_class = PedidoExport
    inlines = [MaterialPedidoInline,]
    list_display = ('codigo_pedido','obra','user','created','validated')
    search_fields = ('obra__name','user__username','user__groups__name', 'memoria') 
    list_filter = ('validated','user__username','obra__name')
    #filter_horizontal = ['materiales']
    def save_model(self, request, obj, form, change): # Asignamos el usuario que ha iniciado sesion
        if not obj.user:
            obj.user = request.user
        obj.save()
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Directores').exists():
            return ['obra','memoria','user','created'] # Solo el campo 'validated' puede ser modificado
        else:
            if obj and obj.validated: # Si el pedido ya ha sido validado no se puede modificar
                return ['obra','memoria','user','validated','created'] 
            return ['validated','user']  # Si no hay pedidos validados, Los campos 'validated' y 'user' serán de solo lectura
    def get_queryset(self, request): # filtramos el queryset para que solo aparezcan las obras del usuario que ha iniciado sesion
        queryset = super().get_queryset(request)
        if request.user.is_authenticated:
            if request.user.groups.filter(name='Tecnicos').exists(): 
                queryset = queryset.filter(user=request.user)
                return queryset
            else: 
                return queryset
    def queryset(self, request):
        return super().queryset(request).filter(user__groups__name='Tecnicos').filter(validated=False)
admin.site.register(Pedido,PedidoAdmin)

class ObraAdmin(admin.ModelAdmin):
    list_display = ('name','user','location', 'contacto','movil')
    search_fields = ('name','user__username','user__groups__name')
    list_filter = ('user__groups','name')
admin.site.register(Obra,ObraAdmin)

class materialAdmin(admin.ModelAdmin):
    list_display = ('name','unidad')
    search_fields = ('name',)
    list_filter = ('name',)
admin.site.register(Material,materialAdmin)

admin.site.register(Sector)

