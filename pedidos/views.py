from .models import Pedido, Obra
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CrearObra, PedidoForm, PedidoFormDir
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
# Librerias para exportar pedidos a excel
from django.db.models import Sum
from django.http import HttpResponse
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment

def index(request):
    saludo = 'Portal de Pedidos'
    creador = 'Lucas L.'
    if (request.user.groups.filter(name__in=['Tecnicos','Lucas']).exists()):
        pedidos = Pedido.objects.filter(user=request.user)
        cant_pedidos = len(pedidos)
        pedidos_aprobados = len(pedidos.filter(validated=True))
        pedidos_pendientes = len(pedidos.filter(validated=False))
        pedidos_comprados = len(pedidos.filter(a_proveedor=True))
        pedidos_no_comprados = len(pedidos.filter(a_proveedor=False))
        try:
            porc_no_comprados = round((pedidos_no_comprados / pedidos_aprobados)*100,1)
            porc_comprados = round((pedidos_comprados / pedidos_aprobados)*100,1)
            porc_aprobados = round((pedidos_aprobados / cant_pedidos)*100,1)
            porc_pendientes = round((pedidos_pendientes / cant_pedidos)*100,1)
        except:
            porc_no_comprados = 0
            porc_comprados = 0
            porc_aprobados = 0
            porc_pendientes = 0
        return render(request, 'index.html', {
            'titulo': saludo,
            'creador': creador,
            'cant_pedidos': cant_pedidos,
            'pedidos_aprobados': pedidos_aprobados,
            'pedidos_pendientes': pedidos_pendientes,
            'porc_aprobados': porc_aprobados,
            'porc_pendientes': porc_pendientes,
            'porc_comprados': porc_comprados,
            'pedidos_comprados': pedidos_comprados,
            'pedidos_no_comprados': pedidos_no_comprados,
            'porc_no_comprados': porc_no_comprados
        })
    elif (request.user.groups.filter(name__in=['Compras','Directores']).exists()):
        pedidos = Pedido.objects.all().order_by('materialespedido__pedido__created')

        pedidos_mes = pedidos.values('materialespedido__pedido__id','materialespedido__pedido__created','materialespedido__pedido__validated','materialespedido__pedido__a_proveedor')
        pedidos_mes = list(pedidos_mes)
        df = pd.DataFrame(pedidos_mes)
        pedidos_mes_group = df.groupby([pd.Grouper(key='materialespedido__pedido__created', freq='ME')]).agg({'materialespedido__pedido__id': 'count','materialespedido__pedido__validated': 'sum', 'materialespedido__pedido__a_proveedor': 'sum'})
        pedidos_mes_group['var_mens_ped'] = round(pedidos_mes_group['materialespedido__pedido__id'].pct_change()*100,1)
        var_pedido=pedidos_mes_group.at[pedidos_mes_group.index[0], 'var_mens_ped']
        cant_pedidos = len(pedidos)

        pedidos_aprobados = len(pedidos.filter(validated=True))
        pedidos_pendientes = len(pedidos.filter(validated=False))
        pedidos_comprados = len(pedidos.filter(a_proveedor=True))
        pedidos_no_comprados = len(pedidos.filter(a_proveedor=False, validated=True))

        try:
            porc_aprobados = round((pedidos_aprobados / cant_pedidos)*100,1)
            porc_pendientes = round((pedidos_pendientes / cant_pedidos)*100,1)
            porc_comprados = round((pedidos_comprados / pedidos_aprobados)*100,1)
            porc_no_comprados = round((pedidos_no_comprados / pedidos_aprobados)*100,1)
        except:
            porc_aprobados=0
            porc_pendientes=0
            porc_comprados=0
            porc_no_comprados=0
        return render(request, 'index.html', {
            'titulo': saludo,
            'creador': creador,
            'cant_pedidos': cant_pedidos,
            'pedidos_aprobados': pedidos_aprobados,
            'pedidos_pendientes': pedidos_pendientes,
            'porc_aprobados': porc_aprobados,
            'porc_pendientes': porc_pendientes,
            'porc_comprados': porc_comprados,
            'pedidos_comprados': pedidos_comprados,
            'pedidos_no_comprados': pedidos_no_comprados,
            'porc_no_comprados': porc_no_comprados,
            'var_pedido': var_pedido
        })
    return render(request, 'index.html', {
            'titulo': saludo,
            'creador': creador,
        })

@login_required
def obra(request):
    obras = Obra.objects.filter(user=request.user)
    return render(request, 'obra.html', {'obras': obras, })
@login_required
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
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Compras','Lucas']).exists())
def pedidos(request):
    pedidos = Pedido.objects.filter(validated=True).order_by('a_proveedor', 'id')
    queryset = request.GET.get('buscar')
    if queryset:
        pedidos = Pedido.objects.filter(
            Q(obra__name__icontains=queryset) |
            Q(user__username__icontains=queryset)|
            Q(orden_compra__icontains=queryset)|
            Q(id__icontains=queryset),
            validated=True).distinct().order_by('a_proveedor', 'id')
    return render(request, 'pedido.html', {'pedidos': pedidos, })
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Directores','Lucas']).exists())
def pedidosDir(request):
    pedidos = Pedido.objects.all().order_by('validated', 'id')
    queryset = request.GET.get('buscar')
    if queryset:
        pedidos = Pedido.objects.filter(
            Q(obra__name__icontains=queryset) |
            Q(user__username__icontains=queryset)|
            Q(orden_compra__icontains=queryset)|
            Q(id__icontains=queryset)|
            Q(memoria__icontains=queryset),
            ).distinct().order_by('validated', 'id')
    return render(request, 'pedidoDir.html', {'pedidos': pedidos, })
@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Compras','Lucas']).exists())
def pedidos_materialespedido(request, pedido_id):
    pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
    # Agrupar los pedidos por obra y material
    pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido','materialespedido__pedido__user__username' ,'materialespedido__material__name','materialespedido__material__unidad','materialespedido__pedido__obra__name', 'materialespedido__material__rubro__name').annotate(cantidad=Sum('materialespedido__cantidad')).order_by('materialespedido__material__rubro__name', 'materialespedido__material__name')
    # Convertir el resultado a una lista
    pedidos_materialespedido = list(pedidos_agrupados)
    obra_name = pedidos_materialespedido[0]['materialespedido__pedido__obra__name'].title()
    cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
    ubicacion = pedidos_materiales.values_list('materialespedido__pedido__obra__localidad')[0][0].title()+', Dpto. '+pedidos_materiales.values_list('materialespedido__pedido__obra__dpto')[0][0].title()
    if request.method == 'GET':
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        form = PedidoForm(instance=pedido)
        return render(request, 'pedidos_materialespedido.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            'form': form,
            'obra_name': obra_name,
            'cod_pedido': cod_pedido,
            'ubicacion': ubicacion
            })
    else:
        try:
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form = PedidoForm(request.POST, instance=pedido)
            form.save()
            return redirect('pedidos')
        except ValueError:
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form = PedidoForm(instance=pedido)
            return render(request, 'pedidos_materialespedido.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            'form': form,
            'obra_name': obra_name,
            'cod_pedido': cod_pedido,
            'ubicacion': ubicacion,
            'error': 'Cod de pedido ya existe.'
            })

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Directores','Lucas']).exists())
def pedidos_materialespedidoDir(request, pedido_id):
    pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
    # Agrupar los pedidos por obra y material
    pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido','materialespedido__pedido__user__username' ,'materialespedido__material__name','materialespedido__material__unidad','materialespedido__pedido__obra__name', 'materialespedido__material__rubro__name', 'materialespedido__sector__name').annotate(cantidad=Sum('materialespedido__cantidad')).order_by('materialespedido__sector__name','materialespedido__material__name')
    # Convertir el resultado a una lista
    pedidos_materialespedido = list(pedidos_agrupados)
    obra_name = pedidos_materialespedido[0]['materialespedido__pedido__obra__name'].title()
    cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
    a_proveedor = pedidos_materiales.values_list('materialespedido__pedido__a_proveedor')[0][0]
    ubicacion = pedidos_materiales.values_list('materialespedido__pedido__obra__localidad')[0][0].title()+', Dpto. '+pedidos_materiales.values_list('materialespedido__pedido__obra__dpto')[0][0].title()
    memoria = pedidos_materiales.values_list('materialespedido__pedido__memoria')[0][0]
    if request.method == 'GET':
        pedido = get_object_or_404(Pedido, pk=pedido_id)
        form = PedidoFormDir(instance=pedido)
        return render(request, 'pedidos_materialespedidoDir.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            'form': form,
            'obra_name': obra_name,
            'cod_pedido': cod_pedido,
            'a_proveedor': a_proveedor,
            'ubicacion': ubicacion,
            'memoria': memoria
            })
    else:
        try:
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form = PedidoFormDir(request.POST, instance=pedido)
            form.save()
            return redirect('pedidosDir')
        except ValueError:
            pedido = get_object_or_404(Pedido, pk=pedido_id)
            form = PedidoFormDir(instance=pedido)
            return render(request, 'pedidos_materialespedidoDir.html', {
            'pedidos_materialespedido': pedidos_materialespedido,
            'form': form,
            'obra_name': obra_name,
            'cod_pedido': cod_pedido,
            'a_proveedor': a_proveedor,
            'ubicacion': ubicacion,
            'memoria': memoria,
            'error': 'Error al validar pedido.'
            })
@login_required
def generar_archivo_xls(request,pedido_id): 
    try:
        pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
        # Agrupar los pedidos por obra y material
        pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido__obra__name','materialespedido__pedido__user__username','materialespedido__pedido','materialespedido__material__name','materialespedido__material__unidad','materialespedido__material__rubro__name',).annotate(cantidad=Sum('materialespedido__cantidad'))
        # Convertir el resultado a una lista
        pedidos_materialespedido = list(pedidos_agrupados)
        pedidos_df = pd.DataFrame(pedidos_materialespedido)
        cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
        df = pedidos_df.rename(columns={'materialespedido__pedido__obra__name':'Obra','materialespedido__pedido':'Pedido N°','materialespedido__material__name':'Descripción','materialespedido__material__unidad':'Unidad de medida','cantidad':'Cantidad','materialespedido__material__rubro__name':'Observaciones'})
        df = df[['Descripción','Unidad de medida','Cantidad','Observaciones']]
        df = df.sort_values(['Observaciones','Descripción'])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="Pedido {pedidos_df["materialespedido__pedido__obra__name"][0].title()}.xlsx"'
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
@login_required
def generar_archivo_xlsDir(request,pedido_id): 
    try:
        pedidos_materiales = Pedido.objects.filter(pk=pedido_id)
        # Agrupar los pedidos por obra y material
        pedidos_agrupados = pedidos_materiales.values('materialespedido__pedido__obra__name','materialespedido__pedido__user__username','materialespedido__pedido','materialespedido__material__name','materialespedido__material__unidad','materialespedido__sector__name').annotate(cantidad=Sum('materialespedido__cantidad'))
        # Convertir el resultado a una lista
        pedidos_materialespedido = list(pedidos_agrupados)
        pedidos_df = pd.DataFrame(pedidos_materialespedido)
        cod_pedido = 'P'+str(pedidos_materialespedido[0]['materialespedido__pedido'])+pedidos_materialespedido[0]['materialespedido__pedido__user__username'][:4].upper()
        df = pedidos_df.rename(columns={'materialespedido__pedido__obra__name':'Obra','materialespedido__pedido':'Pedido N°','materialespedido__material__name':'Material','materialespedido__material__unidad':'Unidad','cantidad':'Cant. Solicitada','materialespedido__sector__name':'Sector'})
        # df = df['Pedido N°'] == pk
        df = df[['Sector','Material','Unidad','Cant. Solicitada']]
        df = df.sort_values(['Sector','Material'])
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
        return redirect('pedidos_detalle_dir')

def es_comprador_o_director(user):
    return user.groups.filter(name__in=["Compras", "Directores"]).exists()
