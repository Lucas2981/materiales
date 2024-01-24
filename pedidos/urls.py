from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',views.obra, name='obras'),
    path('createobras/',views.create_obras, name='crear_obra' ),
    path('pedidos/',views.pedido, name='pedidos' ),
    path('createpedido/',views.create_pedidos, name='crear_pedido' ),
]