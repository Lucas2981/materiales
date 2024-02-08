from import_export import resources
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import Obra, Sector, Material, Pedido,MaterialesPedido, Rubros

class MaterialPedidoInline(admin.TabularInline):
    model = MaterialesPedido
    extra = 1
    autocomplete_fields = ['material']
    def get_readonly_fields(self, request, obj=None):
        if obj and obj.validated:  # condicionamos que solo el campo 'materiales' sea modificado en caso de no estar validado por el director
            return ['material', 'sector', 'cantidad']
        return super().get_readonly_fields(request, obj)  
    def has_delete_permission(self, request, obj=None):
        if obj and obj.validated:
            return False
        return super().has_delete_permission(request, obj)  
class PedidoExport(resources.ModelResource):
    class Meta:
        fields = ('id','obra','user','memoria','created','validated','materiales')
        model = Pedido
class PedidoAdmin(ImportExportModelAdmin):
    resource_class = PedidoExport
    inlines = [MaterialPedidoInline,]
    list_display = ('codigo_pedido','obra','user','created','validated', 'a_proveedor', 'orden_compra')
    search_fields = ('obra__name','user__username','user__groups__name', 'memoria') 
    list_filter = ('validated','a_proveedor','obra__area','user__username','obra__name')
    #filter_horizontal = ['materiales']
    def save_model(self, request, obj, form, change): # Asignamos el usuario que ha iniciado sesion
        if not obj.user:
            obj.user = request.user
        obj.save()
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Directores').exists():
            if obj and obj.a_proveedor: # Si el pedido ya ha sido enviado a proveedor no se puede modificar en direcciones
                return ['obra','memoria','user','validated','a_proveedor','orden_compra']
            else:
                return ['obra','memoria','user','created', 'a_proveedor','orden_compra'] # Solo el campo 'validated' puede ser modificado
        elif request.user.groups.filter(name='Compras').exists():
            if obj and obj.validated: # Si el pedido ya ha sido validado no se puede modificar
                return ['obra','memoria','user','validated','created'] 
        else:
            if obj and obj.validated: # Si el pedido ya ha sido validado no se puede modificar
                return ['obra','memoria','user','validated','created','a_proveedor','orden_compra'] 
            return ['validated','user','a_proveedor','orden_compra']  # Si no hay pedidos validados, Los campos 'validated' y 'user' serán de solo lectura
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
    list_filter = ('name','area' )
admin.site.register(Obra,ObraAdmin)
class materialAdmin(ImportExportModelAdmin):
    list_display = ('id','name','unidad','rubro','referencia')
    search_fields = ('name','referencia', 'id')
    list_filter = ('rubro',)
class MaterialExport(resources.ModelResource):
    class Meta:
        fields = ('name','unidad','rubro','referencia','rubro__name')
        model = Material
admin.site.register(Material,materialAdmin)
admin.site.register(Sector)

class RubrosAdmin(admin.ModelAdmin):
    list_display = ('name','id','referencia')
    search_fields = ('name',)
admin.site.register(Rubros,RubrosAdmin)