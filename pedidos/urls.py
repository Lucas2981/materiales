from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('obras/',views.obra, name='obras'),
    path('createobras/',views.create_obras, name='crear_obra' ),
    path('pedidos/',views.pedido, name='pedidos' ),
    path('createpedido/',views.create_pedidos, name='crear_pedido' ),
    path('signup/',views.signup, name='signup' ),
    path('logout/',views.logout_, name='logout'),
    path('signin/',views.signin, name='signin'),
]