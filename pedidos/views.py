from .models import Obra
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearObra
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas Leiva'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador
    })

def obra(request):
    #obras = Obra.objects.all()
    obras = Obra.objects.filter(user=request.user) #se puede agregar mas filtros separados de la coma
    return render(request,'obra.html', {'obras': obras,})

def create_obras(request):
    if request.method == 'GET':
        return render(request, 'create_obras.html', {
            'form': CrearObra
        })
    else:
        form=CrearObra(request.POST)
        nueva_obra = form.save(commit=False)
        nueva_obra.user = request.user
        nueva_obra.save()
        return redirect('obras')

# @login_required
# def pedido(request):
#     pedidos = IniciarPedidoSector.objects.filter(user=request.user)
#     return render(request,'pedido.html',{'pedidos':pedidos})

# @login_required
# def create_pedidos(request):
#     if request.method == 'GET':
#         return render(request, 'create_pedido.html', {
#             'form': CrearPedido
#         })
#     else:
#         form=CrearPedido(request.POST)
#         nuevo_pedido = form.save(commit=False)
#         nuevo_pedido.user = request.user
#         nuevo_pedido.save()
#         return redirect('crear_pedido')
    
