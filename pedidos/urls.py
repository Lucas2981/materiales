from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',login_required(views.obra), name='obras'),
    path('createobras/',login_required(views.create_obras), name='crear_obra'),
    path('pedidos/<int:pedido_id>/',login_required(views.pedidos_materialespedido), name='pedidos_detalle'),
    path('pedidos/aprobar/<int:pedido_id>/',login_required(views.pedidos_materialespedidoDir), name='pedidos_detalle_dir'),
    path('pedidos/<int:pedido_id>/descargar/', login_required(views.generar_archivo_xls), name='descargar'),
    path('pedidos/aprobar/<int:pedido_id>/descargar/sectores', login_required(views.generar_archivo_xlsDir), name='descargar_sectores'),
    path('pedidos/compras',login_required(views.pedidos), name='pedidos'),
    path('pedidos/aprobar',login_required(views.pedidosDir), name='pedidosDir'),
    # path('createpedido/',login_required(views.create_pedidos), name='crear_pedido'),
]