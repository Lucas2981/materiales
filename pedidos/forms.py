from django.forms import ModelForm
from .models import Obra


class CrearObra(ModelForm):
    class Meta:
        model = Obra
        fields = ['name','location','area','contacto','movil']

# class CrearPedido(ModelForm):
#     class Meta:
#         model = IniciarPedidoSector
#         fields = ['name','sector','materiales']
#     def __init__(self, request, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['user'].initial = request.user