from .models import Pedido, Obra
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearObra, PedidoForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
# Librerias para exportar pedidos a excel
from django.db.models import Sum
from django.http import HttpResponse
import pandas as pd


def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas Leiva'
    return render(request, 'index.html', {
        'titulo': saludo,
        'creador': creador
    })

def obra(request):
    # obras = Obra.objects.all()
    # se puede agregar mas filtros separados de la coma
    obras = Obra.objects.filter(user=request.user)
    return render(request, 'obra.html', {'obras': obras, })

def create_obras(request):
    if request.method == 'GET':
        return render(request, 'create_obras.html', {
            'form': CrearObra
        })
    else:
        form = CrearObra(request.POST)
        nueva_obra = form.save(commit=False)
        nueva_obra.user = request.user
        nueva_obra.save()
        return redirect('obras')

def pedidos(request):
    pedidos = Pedido.objects.filter(validated=True).order_by('a_proveedor', 'id')
    return render(request, 'pedido.html', {'pedidos': pedidos, })
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Compras','Directores']).exists())
def pedidos_materialespedido(request, pedido_id):
    # Obtener todos los pedidos de materiales
    pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
    # Agrupar los pedidos por obra y material
    pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido','materialespedido__pedido__user__username' ,'materialespedido__material__name','materialespedido__material__unidad','materialespedido__pedido__obra__name').annotate(cantidad=Sum('materialespedido__cantidad'))
    # Convertir el resultado a una lista
    pedidos_materialespedido = list(pedidos_agrupados)
    obra_name = pedidos_materialespedido[0]['materialespedido__pedido__obra__name'].capitalize()
    cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
    if request.user.groups.filter(name='Directores').exists():
        return render(request, 'pedidos_materialespedido.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            'obra_name': obra_name,
            'cod_pedido': cod_pedido,
            })
    else:
        if request.method == 'GET':
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form = PedidoForm(instance=pedido)
            return render(request, 'pedidos_materialespedido.html', {
                'pedidos_materialespedido': pedidos_materialespedido,
                'form': form,
                'obra_name': obra_name,
                'cod_pedido': cod_pedido,
                })
        else:
            try:
                pedido = get_object_or_404(Pedido, pk=pedido_id)
                form = PedidoForm(request.POST, instance=pedido)
                form.save()
                return redirect('pedidos')
            except ValueError:
                return render(request, 'pedidos_materialespedido.html', {
                    'pedidos_materialespedido': pedidos_materialespedido,
                    'form': form,
                    'error': 'Error al editar el pedido.'
                })
def generar_archivo_xls(request,pedido_id):
    try:
        # Obtener todos los pedidos de materiales
        pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
        # Agrupar los pedidos por obra y material
        pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido__obra__name','materialespedido__pedido__user__username','materialespedido__pedido','materialespedido__material__name','materialespedido__material__unidad').annotate(cantidad=Sum('materialespedido__cantidad'))
        # Convertir el resultado a una lista
        pedidos_materialespedido = list(pedidos_agrupados)
        pedidos_df = pd.DataFrame(pedidos_materialespedido)
        cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
        df = pedidos_df.rename(columns={'materialespedido__pedido__obra__name':'Obra','materialespedido__pedido':'Pedido N°','materialespedido__material__name':'Material','materialespedido__material__unidad':'Unidad','cantidad':'Cant. Solicitada'})
        # df = df['Pedido N°'] == pk
        df = df[['Obra','Material','Unidad','Cant. Solicitada']]
        df = df.sort_values('Material')
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="pedido_{pedidos_df["materialespedido__pedido__obra__name"][0]}.xlsx"'
        writer = pd.ExcelWriter(response)
        df.to_excel(writer, sheet_name=cod_pedido, index=False)
        for column in df:
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            writer.sheets[cod_pedido].set_column(col_idx, col_idx, column_width)
        writer.close()
        return response
    except:
        return redirect('pedidos_detalle')

def es_comprador_o_director(user):
    return user.groups.filter(name__in=["Compras", "Directores"]).exists()
