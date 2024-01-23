from .models import Obra,IniciarPedidoSector
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearObra, CrearPedido
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

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
#        Obra.objects.create(name=request.POST['name'],
#                           location=request.POST['location'],
#                            area=request.POST['area'],
#                            contacto=request.POST['contacto'],
#                            telefono=request.POST['telefono'])
        form=CrearObra(request.POST)
        nueva_obra = form.save(commit=False)
        nueva_obra.user = request.user
        nueva_obra.save()
        return redirect('obras')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm()
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm(),
                    'error': 'Nombre de usuario ya existe, intente otro nombre'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm(),
            'error': 'Contraseñas no coinciden'
        })


def logout_(request):
    logout(request)
    return redirect('index')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form': AuthenticationForm,
            'error':'Usuario o contraseña incorrecto'
            })
        else:
            login(request,user)
            return redirect('index')

def pedido(request):
    pedidos = IniciarPedidoSector.objects.filter(user=request.user)
    return render(request,'pedido.html',{'pedidos':pedidos})

def create_pedidos(request):
    if request.method == 'GET':
        return render(request, 'create_pedido.html', {
            'form': CrearPedido
        })
    else:
        form=CrearPedido(request.POST)
        nuevo_pedido = form.save(commit=False)
        nuevo_pedido.user = request.user
        nuevo_pedido.save()
        return redirect('crear_pedido')
    
