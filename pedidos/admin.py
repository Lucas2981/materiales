from django.contrib import admin
from .models import Obra, Sector, Material, Pedido,MaterialesPedido

class MaterialPedidoInline(admin.TabularInline):
    model = MaterialesPedido
    extra = 1
    autocomplete_fields = ['material']
    
class PedidoAdmin(admin.ModelAdmin):
    inlines = [MaterialPedidoInline,]
    list_display = ('obra', 'sector', 'user','created','validated')
    search_fields = ('obra__name','user__username','user__groups__name', 'sector__name') 
    list_filter = ('validated','user__username','obra__name')
    #filter_horizontal = ['materiales']
    def save_model(self, request, obj, form, change): # Asignamos el usuario que ha iniciado sesion
        if not obj.user:
            obj.user = request.user
        obj.save()
    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name='Directores').exists():
            return ['obra','sector','user','created','validated','materiales'] # Solo el campo 'validated' puede ser modificado
        else:
            if obj and obj.validated: # Si el pedido ya ha sido validado no se puede modificar
                return ['obra','sector','materiales','description','user','validated','created'] 
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

