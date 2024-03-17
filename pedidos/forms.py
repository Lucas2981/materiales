from django.forms import ModelForm
from .models import Obra, Pedido
from django import forms



class CrearObra(ModelForm):
    class Meta:
        model = Obra
        fields = ['name','location','area']

class PedidoForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['a_proveedor','orden_compra']
    
class PedidoFormDir(ModelForm):
    class Meta:
        model = Pedido
        fields = ['validated']

class MemoriaForm(ModelForm):
    class Meta:
        model = Pedido
        fields = ['problema','propuesta','memoria']