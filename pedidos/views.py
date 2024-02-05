from .models import Pedido, Obra, Material, MaterialesPedido
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearObra
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Librerias para exportar pedidos a excel
from django.db.models import Sum
from django.http import HttpResponse
# from openpyxl import Workbook
import xlsxwriter
import tempfile
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
    pedidos = Pedido.objects.all()
    return render(request, 'pedido.html', {'pedidos': pedidos, })

def pedidos_materialespedido(request):
    # Obtener todos los pedidos de materiales
    pedidos_materiales = Pedido.objects.all()
    # Agrupar los pedidos por obra y material
    pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido','materialespedido__pedido__user__username' ,'materialespedido__material__name','materialespedido__material__unidad').annotate(cantidad=Sum('materialespedido__cantidad'))
    # Convertir el resultado a una lista
    pedidos_materialespedido = list(pedidos_agrupados)
    if request.method == 'GET':
        # Renderizar la plantilla con los datos agrupados
        return render(request, 'pedidos_materialespedido.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            })
    else:  
        return generar_archivo_xls(pedidos_materialespedido)

def generar_archivo_xls(request):
    # Obtener todos los pedidos de materiales
    pedidos_materiales = Pedido.objects.all()
    # Agrupar los pedidos por obra y material
    pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido__obra__name','materialespedido__pedido','materialespedido__pedido__user__username' ,'materialespedido__material__name','materialespedido__material__unidad').annotate(cantidad=Sum('materialespedido__cantidad'))
    # Convertir el resultado a una lista
    pedidos_materialespedido = list(pedidos_agrupados)
    pedidos_df = pd.DataFrame(pedidos_materialespedido)
    df = pedidos_df.rename(columns={'materialespedido__pedido__obra__name':'Obra','materialespedido__pedido':'Pedido N°','materialespedido__pedido__user__username':'Tec. Solicitante','materialespedido__material__name':'Material','materialespedido__material__unidad':'Unidad','cantidad':'Cant. Solicitada'})
    def truncate_technician(name):
        if len(name) > 4:
            return name[:4].upper()
        else:
            return name.upper()
    df['Cod. Pedido'] = 'P' + df['Pedido N°'].astype(str) + df['Tec. Solicitante'].apply(truncate_technician)
    # df_group = df.groupby(['Cod. Pedido','Obra','Material','Unidad']).agg({'cantidad':'sum'}).reset_index()
    df = df[['Cod. Pedido','Obra','Material','Unidad','Cant. Solicitada']]
    df = df.sort_values('Cod. Pedido')
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="pedido_{pedidos_df["materialespedido__pedido__obra__name"][0]}.xlsx"'
    writer = pd.ExcelWriter(response)
    df.to_excel(writer, sheet_name=df["Cod. Pedido"][0], index=False)
    for column in df:
        column_width = max(df[column].astype(str).map(len).max(), len(column))
        col_idx = df.columns.get_loc(column)
        writer.sheets[df["Cod. Pedido"][0]].set_column(col_idx, col_idx, column_width)
    writer.close()
    return response
