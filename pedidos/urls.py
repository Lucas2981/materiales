from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',login_required(views.obra), name='obras'),
    path('createobras/',login_required(views.create_obras), name='crear_obra'),
    path('pedidos/<int:pedido_id>/',login_required(views.pedidos_materialespedido), name='pedidos_detalle'),
    path('pedidos/<int:pedido_id>/descargar/', login_required(views.generar_archivo_xls), name='descargar'),
    path('pedidos/',login_required(views.pedidos), name='pedidos'),
    # path('createpedido/',login_required(views.create_pedidos), name='crear_pedido'),
]