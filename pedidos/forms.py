from django.forms import ModelForm
from .models import Obra, IniciarPedidoSector


class CrearObra(ModelForm):
    class Meta:
        model = Obra
        fields = ['obra','ubicacion','area','contacto','telefono']

class CrearPedido(ModelForm):
    class Meta:
        model = IniciarPedidoSector
        fields = ['obra','sector','material','cantidad']
