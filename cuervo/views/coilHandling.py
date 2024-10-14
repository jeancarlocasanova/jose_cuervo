from django.shortcuts import render, redirect, get_object_or_404
from ..models import coilStatus, coilType, coilProvider, coil, label, init_label, coilsInInventory, order, lot, granel_lot, GranelConsumptionDetail, labelStatus, SKU
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import CoilStatusForm, CoilProviderForm, CoilTypeForm, CreateCoilForm, CreateCoilFormv2, UpdateCoilForm, FilterCoilForm,DeleteLabelForm,FilterCoilFormOrderAsign,Consumo_Manform,Consumo_Envform,AddGranelloteform,NumAsignacionform
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError, IntegerField, Value
from django.forms import formset_factory
from django.db.models.functions import Cast
from django.db.models.expressions import RawSQL
from datetime import datetime, timedelta
from django.db.models import Q, F
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from zeep import Client, Settings
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import pyodbc
from requests import Session

@permission_required('cuervo.view_coilstatus', login_url='/login/')
def coilHandling_view(request):
    return render(request, "cuervo/coilHandling.html")

# <------ COIL STATUS CRUD --------!>
def coilStatus_view(request):
    coil_status = coilStatus.objects.all()
    return render(request, "cuervo/coilStatus.html", {'coil_status': coil_status})

class deleteCoilStatus_view(PermissionRequiredMixin, DeleteView):
    model = coilStatus
    template_name = 'cuervo/coil_status_confirm_delete.html'
    success_url = reverse_lazy('coilStatus')
    permission_required = 'cuervo.delete_coilstatus'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tittle = "A ocurrido un error"
        msg = "No se puede eliminar este dato debido a que esta asignado a un registro"
        isError = False
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            isError = True
        finally:
            if(isError):
                return render(request, "cuervo/display_error.html", {"tittle": tittle, "msg": msg, "link": success_url})
            else:
                return redirect(success_url)

class updateCoilStatus_view(PermissionRequiredMixin, UpdateView):
    model = coilStatus
    template_name = 'cuervo/coil_status_edit.html'
    success_url = reverse_lazy('coilStatus')
    fields = ['name', 'description']
    permission_required = 'cuervo.change_coilstatus'

@permission_required('cuervo.add_coilstatus', login_url='/login/')
def createCoilStatus_view(request):
    msg = None
    if request.method == "POST":
        form = CoilStatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                coilStatusObj = coilStatus.objects.get(name=name)
            except:
                coilStatusObj = None

            if coilStatusObj is None:
                coilStatusObj = coilStatus.objects.create(name=name, description=description)
                coilStatusObj.save()
                return redirect("/coilStatus/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = CoilStatusForm()

    return render(request, "cuervo/coil_status_create.html", {"form": form, "msg": msg})

# <------ COIL TYPE CRUD --------!>
@permission_required('cuervo.view_coiltype', login_url='/login/')
def coilType_view(request):
    coil_type = coilType.objects.all()
    return render(request, "cuervo/coilType.html", {'coil_type': coil_type})

class deleteCoilType_view(PermissionRequiredMixin, DeleteView):
    model = coilType
    template_name = 'cuervo/coil_type_confirm_delete.html'
    success_url = reverse_lazy('coilType')
    permission_required = 'cuervo.delete_coiltype'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tittle = "A ocurrido un error"
        msg = "No se puede eliminar este dato debido a que esta asignado a un registro"
        isError = False
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            isError = True
        finally:
            if(isError):
                return render(request, "cuervo/display_error.html", {"tittle": tittle, "msg": msg, "link": success_url})
            else:
                return redirect(success_url)

class updateCoilType_view(PermissionRequiredMixin, UpdateView):
    model = coilType
    template_name = 'cuervo/coil_type_edit.html'
    success_url = reverse_lazy('coilType')
    fields = ['name']
    permission_required = 'cuervo.change_coiltype'

@permission_required('cuervo.add_coiltype', login_url='/login/')
def createCoilType_view(request):
    msg = None
    if request.method == "POST":
        form = CoilTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            try:
                coilTypeObj = coilType.objects.get(name=name)
            except:
                coilTypeObj = None

            if coilTypeObj is None:
                coilTypeObj = coilType.objects.create(name=name)
                coilTypeObj.save()
                return redirect("/coilType/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = CoilTypeForm()

    return render(request, "cuervo/coil_type_create.html", {"form": form, "msg": msg})

# <------ COIL PROVIDER CRUD --------!>
@permission_required('cuervo.view_coilprovider', login_url='/login/')
def coilProvider_view(request):
    coil_provider = coilProvider.objects.all()
    return render(request, "cuervo/coilProvider.html", {'coil_provider': coil_provider})

class deleteCoilProvider_view(PermissionRequiredMixin, DeleteView):
    model = coilProvider
    template_name = 'cuervo/coil_provider_confirm_delete.html'
    success_url = reverse_lazy('coilProvider')
    permission_required = 'cuervo.delete_coilprovider'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tittle = "A ocurrido un error"
        msg = "No se puede eliminar este dato debido a que esta asignado a un registro"
        isError = False
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            isError = True
        finally:
            if(isError):
                return render(request, "cuervo/display_error.html", {"tittle": tittle, "msg": msg, "link": success_url})
            else:
                return redirect(success_url)

class updateCoilProvider_view(PermissionRequiredMixin, UpdateView):
    model = coilProvider
    template_name = 'cuervo/coil_provider_edit.html'
    success_url = reverse_lazy('coilProvider')
    fields = ['name']
    permission_required = 'cuervo.change_coilprovider'

@permission_required('cuervo.add_coilprovider', login_url='/login/')
def createCoilProvider_view(request):
    msg = None
    if request.method == "POST":
        form = CoilProviderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            try:
                coilProviderObj = coilProvider.objects.get(name=name)
            except:
                coilProviderObj = None

            if coilProviderObj is None:
                coilProviderObj = coilProvider.objects.create(name=name)
                coilProviderObj.save()
                return redirect("/coilProvider/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = CoilProviderForm()

    return render(request, "cuervo/coil_provider_create.html", {"form": form, "msg": msg})

# <------ COIL CRUD --------!>
@permission_required('cuervo.view_coil', login_url='/login/')
def coil_view(request):
    coilList = coil.objects.all()
    return render(request, "cuervo/coil.html", {'coilList': coilList})


class updateCoil_view(PermissionRequiredMixin, UpdateView):
    model = coil
    template_name = 'cuervo/coil_edit.html'
    success_url = reverse_lazy('coil')
    form_class = UpdateCoilForm
    permission_required = 'cuervo.change_coil'

    def get_queryset(self):
        # Check if the user has the change_coil permission
        if self.request.user.has_perm('cuervo.change_coil'):
            # User has permission to edit any coil, so return all coils
            return self.model.objects.all()
        else:
            # User doesn't have the permission, filter by last_edit_user
            owner = self.request.user
            return self.model.objects.filter(last_edit_user=owner)
def are_consecutive_rolls(bobinas_seleccionadas):
    if not bobinas_seleccionadas:
        return True  # Si no hay bobinas seleccionadas, no hay restricción de consecutividad

    # Obtener números de rollo ordenados
    bobinas = coil.objects.filter(id__in=bobinas_seleccionadas).order_by('numrollo')
    numeros_rollo = [bobina.numrollo for bobina in bobinas]

    # Verificar si los números de rollo son consecutivos
    return all(numeros_rollo[i] + 1 == numeros_rollo[i + 1] for i in range(len(numeros_rollo) - 1))

@permission_required('auth.assign_coil', login_url='/login/')
def init_coil_create(request):
    msg = None
    orden = None
    bobinas = coil.objects.none()
    selected_order_coils = []
    marbetes_necesarios = 0
    marbetes_totales = 0
    bobinas_solicitadas = set()
    form_filter = FilterCoilFormOrderAsign()

    try:


        if request.method == "POST":
            form = CreateCoilFormv2(request.POST)
            form_filter = FilterCoilFormOrderAsign(request.POST)

            if 'buscar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    if orden.status == 'REL' or orden.status == 'CRTD':
                        selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                        # Obtener la submarca del SKU de la orden de producción
                        sku_subtype_id = orden.FK_sku_id.Fk_sku_subtype_id.id if orden.FK_sku_id.Fk_sku_subtype_id else None

                        print(sku_subtype_id)

                        if sku_subtype_id:
                            # Obtener bobinas asociadas a la submarca del SKU
                            bobinas_ids = coil.objects.filter(Fk_sku_subtype_id=sku_subtype_id).values_list('id',
                                                                                                            flat=True)

                            # Bobinas asignadas (solo las asignadas no solicitadas)
                            bobinas_asignadas = coil.objects.filter(
                                id__in=selected_order_coils,
                                FK_coilStatus_id__name='Asignada'
                            )

                            # Bobinas disponibles (estado 'Sin asignar' o 'Devuelta'), excluyendo 'Solicitada'
                            bobinas_disponibles = coil.objects.filter(
                                id__in=bobinas_ids
                            ).filter(
                                Q(FK_coilStatus_id__name='Disponible') | Q(FK_coilStatus_id__name='Devuelta')
                            ).exclude(
                                FK_coilStatus_id__name__in=['Solicitada'] if 'Solicitada' else []
                            )

                            bobinas = (bobinas_disponibles | bobinas_asignadas).order_by('initNumber')

                            bobinas_asignadastotales = coil.objects.filter(
                                id__in=selected_order_coils
                            )

                            # Obtener bobinas solicitadas de las asignadas
                            bobinas_solicitadas = set(
                                bobina.id for bobina in bobinas_asignadastotales.filter(
                                    FK_coilStatus_id__name='Solicitada'
                                )
                            )

                        else:
                            msg = 'No se encontró la submarca del SKU para la orden de producción.'

                    elif orden.status == 'TECO':
                        msg = 'Orden de producción cerrada'

                except order.DoesNotExist:
                    search_order_service()

                    try:
                        orden = order.objects.get(uniqueid=ordenproduccion)

                        if orden.status == 'REL' or orden.status == 'CRTD':
                            selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                            # Obtener la submarca del SKU de la orden de producción
                            sku_subtype_id = orden.FK_sku_id.Fk_sku_subtype_id.id if orden.FK_sku_id.Fk_sku_subtype_id else None

                            print(sku_subtype_id)

                            if sku_subtype_id:
                                # Obtener bobinas asociadas a la submarca del SKU
                                bobinas_ids = coil.objects.filter(Fk_sku_subtype_id=sku_subtype_id).values_list('id',
                                                                                                                flat=True)

                                # Bobinas asignadas (solo las asignadas no solicitadas)
                                bobinas_asignadas = coil.objects.filter(
                                    id__in=selected_order_coils,
                                    FK_coilStatus_id__name='Asignada'
                                )

                                # Bobinas disponibles (estado 'Sin asignar' o 'Devuelta'), excluyendo 'Solicitada'
                                bobinas_disponibles = coil.objects.filter(
                                    id__in=bobinas_ids
                                ).filter(
                                    Q(FK_coilStatus_id__name='Disponible') | Q(FK_coilStatus_id__name='Devuelta')
                                ).exclude(
                                    FK_coilStatus_id__name__in=['Solicitada'] if 'Solicitada' else []
                                )

                                bobinas = (bobinas_disponibles | bobinas_asignadas).order_by('initNumber')

                                bobinas_asignadastotales = coil.objects.filter(
                                    id__in=selected_order_coils
                                )

                                # Obtener bobinas solicitadas de las asignadas
                                bobinas_solicitadas = set(
                                    bobina.id for bobina in bobinas_asignadastotales.filter(
                                        FK_coilStatus_id__name='Solicitada'
                                    )
                                )

                            else:
                                msg = 'No se encontró la submarca del SKU para la orden de producción.'

                        elif orden.status == 'TECO':
                            msg = 'Orden de producción cerrada'

                    except order.DoesNotExist:
                        msg = 'Orden de producción no encontrada'

                    

            elif 'seleccionar' in request.POST and form_filter.is_valid():
                if form_filter.is_valid():

                    marbetes_necesarios = int(request.POST.get('marbetes_necesarios', 0))
                    ordenproduccion = request.POST.get("ordenproduccion")

                    try:
                        orden = order.objects.get(uniqueid=ordenproduccion)

                        if orden.status == 'REL' or orden.status == 'CRTD':
                            selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                            # Obtener la submarca del SKU de la orden de producción
                            sku_subtype_id = orden.FK_sku_id.Fk_sku_subtype_id.id if orden.FK_sku_id.Fk_sku_subtype_id else None

                            if sku_subtype_id:
                                # Obtener bobinas asociadas a la submarca del SKU
                                bobinas_ids = coil.objects.filter(Fk_sku_subtype_id=sku_subtype_id).values_list('id',
                                                                                                                flat=True)

                                # Bobinas asignadas (solo las asignadas no solicitadas)
                                bobinas_asignadas = coil.objects.filter(
                                    id__in=selected_order_coils,
                                    FK_coilStatus_id__name='Asignada'
                                )

                                # Bobinas disponibles (estado 'Sin asignar' o 'Devuelta'), excluyendo 'Solicitada'
                                bobinas_disponibles = coil.objects.filter(
                                    id__in=bobinas_ids
                                ).filter(
                                    Q(FK_coilStatus_id__name='Disponible') | Q(FK_coilStatus_id__name='Devuelta')
                                ).exclude(
                                    FK_coilStatus_id__name__in=['Solicitada'] if 'Solicitada' else []
                                )

                                bobinas = (bobinas_disponibles | bobinas_asignadas).order_by('initNumber')

                                bobinas_asignadastotales = coil.objects.filter(
                                    id__in=selected_order_coils
                                )

                                # Obtener bobinas solicitadas de las asignadas
                                bobinas_solicitadas = set(
                                    bobina.id for bobina in bobinas_asignadastotales.filter(
                                        FK_coilStatus_id__name='Solicitada'
                                    )
                                )

                                total_marbetes = 0
                                selected_bobinas_ids = []
                                for bobina in bobinas:
                                    if total_marbetes < marbetes_necesarios:
                                        total_marbetes += bobina.missing
                                        selected_bobinas_ids.append(bobina.id)

                                for bobina in bobinas:
                                    bobina.selected = bobina.id in selected_bobinas_ids

                                marbetes_totales = total_marbetes

                            else:
                                msg = 'No se encontró la submarca del SKU para la orden de producción.'


                        elif orden.status == 'CTCO':
                            msg = 'Orden de producción cerrada'

                    except order.DoesNotExist:
                        msg = 'Orden de producción no encontrada'

            elif 'crear' in request.POST and form.is_valid():
                bobinas_seleccionadas_str = request.POST.get('current_bobinas', '')
                bobinas_seleccionadas_ids = [int(id) for id in bobinas_seleccionadas_str.split(',') if id.isdigit()]

                initial_bobinas_str = request.POST.get('initial_bobinas', '')
                initial_bobinas_ids = [int(id) for id in initial_bobinas_str.split(',') if id.isdigit()]

                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                orden = order.objects.get(uniqueid=ordenproduccion)

                if not orden:
                    msg = 'Orden de producción no seleccionada.'
                else:
                    bobinas_solicitadas_str = request.POST.get('bobinas_solicitadas', '')
                    bobinas_solicitadas_ids = [int(id) for id in bobinas_solicitadas_str.split(',') if id.isdigit()]

                    bobinas_seleccionadas = coil.objects.filter(id__in=bobinas_seleccionadas_ids)
                    initial_bobinas = coil.objects.filter(id__in=initial_bobinas_ids)
                    bobinas_solicitadas = coil.objects.filter(id__in=bobinas_solicitadas_ids)

                    bobinas_a_desasignar = list(set(initial_bobinas_ids) - set(bobinas_seleccionadas_ids))
                    bobinas_a_asignar = list(set(bobinas_seleccionadas_ids) - set(initial_bobinas_ids))

                    
                    # Desasignar bobinas que ya no están seleccionadas
                    for bobina_id in bobinas_a_desasignar:
                        if bobina_id not in bobinas_solicitadas_ids:
                            bobina = coil.objects.get(id=bobina_id)
                            bobina.FK_coilStatus_id = coilStatus.objects.get(name='Disponible')
                            bobina.save()


                    # Asignar bobinas que están seleccionadas pero no estaban asignadas inicialmente
                    for bobina_id in bobinas_a_asignar:
                        bobina = coil.objects.get(id=bobina_id)
                        bobina.FK_coilStatus_id = coilStatus.objects.get(name='Asignada')
                        bobina.save()

                        # Actualizar la lista de bobinas asignadas en la orden de producción
                    bobinas_actualizadas = list(bobinas_seleccionadas) + list(bobinas_solicitadas)
                    orden.coils = ','.join(str(bobina.id) for bobina in bobinas_actualizadas)
                    orden.save()
                    msg = 'Bobinas actualizadas con éxito en la orden.'
        else:
            form = CreateCoilFormv2()

        return render(request, "cuervo/coil_createv2.html", {
            "form": form,
            "msg": msg,
            "bobinas": bobinas,
            "orden": orden,
            "selected_order_coils": selected_order_coils,
            "bobinas_solicitadas": bobinas_solicitadas,
            "marbetes_necesarios": marbetes_necesarios,
            "marbetes_totales": marbetes_totales,
            "form2": form_filter
        })
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })









# Función para verificar si la fecha es válida
def is_valid_date(date_str):
    try:
        # Intenta convertir la cadena de fecha al formato YYYY-MM-DD
        if date_str and date_str != "0000-00-00":
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        return False
    except ValueError:
        return False


# Función del servicio de búsqueda de una orden específica
def search_order_service():
    wsdl_url = 'http://C1.cuervo.com.mx:8001/sap/bc/srt/wsdl/flv_10002A111AD1/bndg_url/sap/bc/srt/rfc/sap/zfun_ws_ordproc_pp/050/zfun_ws_ordproc_pp/zfun_ws_ordproc_pp?sap-client=050'

    # Configuración de autenticación
    username = 'cvowebservic'
    password = 'Mexico2018+'

    # Calcular el rango de fechas
    fecha_actual = datetime.now()
    fecha_inicio = (fecha_actual - timedelta(days=180)).strftime('%Y-%m-%d')
    fecha_fin = (fecha_actual + timedelta(days=180)).strftime('%Y-%m-%d')

    # Crear una sesión con autenticación
    session = Session()
    session.auth = HTTPBasicAuth(username, password)

    # Configurar el transporte con la sesión
    transport = Transport(session=session)

    # Configuración para evitar redirecciones automáticas
    settings = Settings(strict=False, xml_huge_tree=True)

    # Crear el cliente con la URL del WSDL
    client = Client(wsdl=wsdl_url, transport=transport, settings=settings)

    # Forzar el endpoint a la URL correcta
    for service in client.wsdl.services.values():
        for port in service.ports.values():
            port.binding_options[
                'address'] = 'http://C1.cuervo.com.mx:8001/sap/bc/srt/rfc/sap/zfun_ws_ordproc_pp/050/zfun_ws_ordproc_pp/zfun_ws_ordproc_pp?sap-client=050'
            # port.binding_options['address'] = 'http://DV2.cuervo.com.mx:8000/sap/bc/srt/rfc/sap/zfun_ws_ordenes_pp/050/zfun_ws_ordenes_pp/zfun_ws_ordenes_pp?sap-client=050' PRUEBAS

    # Parámetros de la función
    params = {
        'item': [
            {
                'SIGN': 'I',
                'OPTION': 'BT',
                'LOW': fecha_inicio,
                'HIGH': fecha_fin
            }
        ]
    }

    # Llamar a la función del servicio web con los parámetros adecuados
    try:
        response = client.service.ZFUN_WS_ORDPROC_PP(
            ET_DETALLE=[],  # Tabla vacía inicialmente
            ET_ORDENES=[],  # Tabla vacía inicialmente
            IT_FECHAS=[params],  # Pasar la lista con las fechas
            I_CENTRO='1100',  # Centro
            I_FECHA=''  # Fecha opcional, dejar vacío si no se usa
        )
        # print(response)
    except Exception as e:
        print(f"Error: {e}")

    try:
        conn = pyodbc.connect('DRIVER={SQL Server};SERVER=MBTE-EDI;DATABASE=Cuervo;UID=Mesauto1;PWD=M354ut0%')
        cursor = conn.cursor()
        conn.autocommit = False

        et_ordenes = response['ET_ORDENES']['item']
        et_detalle = response['ET_DETALLE']['item']

        for orden_data in et_ordenes:
            cursor.execute("SELECT id, FK_sku_id_id FROM cuervo_order WHERE uniqueid = ?",
                           (orden_data['ORDEN'].lstrip('0'),))
            existing_order = cursor.fetchone()

            print(f"BUSCANDO ORDEN: {orden_data['ORDEN']}")

            if not existing_order:
                if not orden_data['SKU_PT'] == None:
                    # Ajustar la consulta de SKU para ignorar ceros iniciales
                    sku_value = orden_data['SKU_PT'].lstrip('0')

                    # Primera consulta simplificada
                    cursor.execute("SELECT id FROM cuervo_sku WHERE sku LIKE ?", (sku_value))
                    sku = cursor.fetchone()
                    print(f"Buscando SKU (sin ceros iniciales): {sku_value}")
                    print(f"Resultado SKU: {sku}")

                    if not sku:
                        print(f"SKU no encontrado: {orden_data['SKU_PT']}")
                    else:
                        cursor.execute("SELECT id FROM cuervo_inventorylocation WHERE description LIKE ?",
                                       (orden_data['LINEA_PRODUC']))
                        inventory_location = cursor.fetchone()

                        line_value = orden_data['LINEA_PRODUC']

                        print(f"Buscando Linea: {line_value}")
                        print(f"Resultado Linea: {inventory_location}")
                        if not inventory_location:
                            print(f"Inventory location no encontrada: {orden_data['LINEA_PRODUC']}")
                        else:
                            for lote_data in et_detalle:
                                if lote_data['ORDEN'] == orden_data['ORDEN']:
                                    print('Orden: ', orden_data['ORDEN'])
                                    print('Orden LOTE: ', lote_data['ORDEN'])
                                    if orden_data['ESTATUS_ORDEN'] == 'REL' or orden_data[
                                        'ESTATUS_ORDEN'] == 'CRTD':  # and lote_data['PROVEEDOR'] == None:
                                        print('SI CUMPLE LAS CONDICIONES DE ORDEN LIBERADA SIN CONSUMO')

                                        init_date = orden_data['FECHA_INICIO'] if is_valid_date(
                                            orden_data['FECHA_INICIO']) else None
                                        finish_date = orden_data['FECHA_FIN'] if is_valid_date(
                                            orden_data['FECHA_FIN']) else None

                                        cursor.execute("""
                                            INSERT INTO cuervo_order (uniqueid, FK_sku_id_id, status, init_date, finish_date, FK_inventoryLocation_id_id)
                                            VALUES (?, ?, ?, ?, ?, ?)
                                        """, (
                                        orden_data['ORDEN'].lstrip('0'), sku[0], orden_data['ESTATUS_ORDEN'], init_date,
                                        finish_date, inventory_location[0]))
                                        conn.commit()

                                        if cursor.rowcount == 1:
                                            cursor.execute("SELECT id FROM cuervo_order WHERE uniqueid = ?",
                                                           (orden_data['ORDEN'].lstrip('0'),))
                                            order_id_db = cursor.fetchone()
                                            if order_id_db:
                                                order_id_db = order_id_db[0]
                                                print(f"Orden insertada: {order_id_db}")
                                            else:
                                                print(
                                                    f"No se encontró la orden {orden_data['ORDEN']} después de la inserción.")
                                        else:
                                            print(f"Fallo al insertar la orden {orden_data['ORDEN']}.")
                                    else:
                                        print('NO CUMPLE LAS CONDICIONES DE ORDEN LIBERADA SIN CONSUMO')
                                        print('Orden: ', orden_data['ORDEN'])
                                        print('STATUS: ', orden_data['ESTATUS_ORDEN'])
                                        print('CONSUMO: ', lote_data['PROVEEDOR'])
                else:

                    print(f"Orden {orden_data['ORDEN']} NO TRAE SKU.")
            else:
                print(f"Orden {orden_data['ORDEN']} ya existe en la base de datos.")

                # Verificar si la orden existente no tiene SKU asignado
                order_id_db, existing_sku_id = existing_order
                if existing_sku_id is None:
                    print(f"La orden {orden_data['ORDEN']} no tiene SKU asignado. Procediendo a buscar y asignar SKU.")

                    if not orden_data['SKU_PT'] == None:
                        sku_value = orden_data['SKU_PT'].lstrip('0')

                        # Buscar el SKU correspondiente
                        cursor.execute("SELECT id FROM cuervo_sku WHERE sku LIKE ?", (f"%{sku_value}%",))
                        sku = cursor.fetchone()
                        print(f"Buscando SKU (sin ceros iniciales): {sku_value}")
                        print(f"Resultado SKU: {sku}")

                        if not sku:
                            print(f"SKU no encontrado: {orden_data['SKU_PT']}")
                        else:
                            # Actualizar la orden con el SKU encontrado
                            cursor.execute("UPDATE cuervo_order SET FK_sku_id_id = ? WHERE id = ?",
                                           (sku[0], order_id_db))
                            conn.commit()

                            if cursor.rowcount == 1:
                                print(f"Orden {orden_data['ORDEN']} actualizada con SKU {sku_value}.")
                            else:
                                print(f"Fallo al actualizar la orden {orden_data['ORDEN']} con SKU {sku_value}.")
                else:
                    print(f"La orden {orden_data['ORDEN']} ya tiene un SKU asignado.")



    except pyodbc.Error as e:
        conn.rollback()
        print("Error de pyodbc:", e)
    finally:
        conn.autocommit = True
        conn.close()














    

@permission_required('cuervo.add_coil', login_url='/login/')
def createCoil_view(request):
    msg = None
    data_exists = None
    issaved = None
    fecha_despues_9_meses = None
    if request.method == "POST":
        form = CreateCoilForm(request.POST)
        if form.is_valid():
            initNumber = form.cleaned_data.get("initNumber")
            finishNumber = form.cleaned_data.get("finishNumber")
            numrollo = form.cleaned_data.get("numrollo")
            boxNumber = form.cleaned_data.get("boxNumber")
            notDelivered = form.cleaned_data.get("notDelivered")
            purchaseOrder = form.cleaned_data.get("purchaseOrder")
            FK_labelStatus_id = form.cleaned_data.get("FK_labelStatus_id")
            orderUniqueid = form.cleaned_data.get("orderUniqueid")
            FK_inventoryLocation_id = form.cleaned_data.get("FK_inventoryLocation_id")
            FK_sku_id = form.cleaned_data.get("FK_sku_id")
            FK_coilStatus_id = form.cleaned_data.get("FK_coilStatus_id")
            FK_coilType_id = form.cleaned_data.get("FK_coilType_id")
            FK_coilProvider_id = form.cleaned_data.get("FK_coilProvider_id")
            last_edit_user = request.user

            # Filter queryset based on the range of uniqueid
            resultados = init_label.objects.annotate(
                            numeric_part_int=Cast(
                                RawSQL(
                                    "TRY_CAST(SUBSTRING(uniqueid, CHARINDEX('-', uniqueid) + 1, CHARINDEX('_', uniqueid + '_', CHARINDEX('-', uniqueid)) - CHARINDEX('-', uniqueid) - 1) AS INT)",
                                    (),
                                ),
                                IntegerField(),
                            )
                            ).filter(
                            numeric_part_int__range=(initNumber, finishNumber)
                            ).values('id', 'uniqueid', 'brand_id', 'file_name', 'url')
            print(resultados)
            try:
                coilObj = coil.objects.filter(
                    numrollo__in=numrollo,
                    FK_coilType_id__in=FK_coilType_id,
                    initNumber__range=(initNumber, finishNumber),
                    finishNumber__range=(initNumber, finishNumber)
                )
            except:
                coilObj = None
            if coilObj is None:
                delivered = len(resultados)
                missing = delivered - notDelivered
                try:
                    coilObj = coil.objects.create(notDelivered=notDelivered,
                                                  finishNumber=finishNumber, initNumber=initNumber,
                                                  numrollo=numrollo, purchaseOrder=purchaseOrder,
                                                  boxNumber=boxNumber, missing=missing,
                                                  FK_sku_id=FK_sku_id, FK_coilStatus_id=FK_coilStatus_id,
                                                  FK_coilType_id=FK_coilType_id,
                                                  FK_coilProvider_id=FK_coilProvider_id,
                                                  last_edit_user=last_edit_user, delivered=delivered,
                                                  orderUniqueid=orderUniqueid)
                    for index, result in enumerate(resultados):
                        data_exists = label.objects.filter(uniqueid=result['uniqueid'], url=result['url'])
                        fecha_actual = datetime.now()
                        # Calcula la fecha después de 9 meses
                        fecha_despues_9_meses = fecha_actual + timedelta(days=9 * 30)
                    if not data_exists:
                        for result in resultados:
                            labelObj = label.objects.create(
                                uniqueid=result['uniqueid'],
                                url=result['url'],
                                FK_coil_id=coilObj,
                                FK_labelStatus_id=FK_labelStatus_id,
                                FK_inventoryLocation_id=FK_inventoryLocation_id,
                                last_edit_user=last_edit_user,
                                expiration=fecha_despues_9_meses
                            )
                        coilObj.save()
                        coilInventory = coilsInInventory.objects.create(notDelivered=notDelivered,
                                                  finishNumber=finishNumber, initNumber=initNumber,
                                                  numrollo=numrollo, purchaseOrder=purchaseOrder,
                                                  boxNumber=boxNumber, missing=missing,
                                                  FK_sku_id=FK_sku_id, FK_coilStatus_id=FK_coilStatus_id,
                                                  FK_coilType_id=FK_coilType_id,
                                                  FK_coilProvider_id=FK_coilProvider_id,
                                                  last_edit_user=last_edit_user, delivered=delivered,
                                                  orderUniqueid=orderUniqueid, FK_coil_id=coilObj)
                        issaved = True
                    else:
                        coil.objects.filter(id=coilObj.id).delete()
                        msg = "Algunos de estos marbetes ya existen"
                except Exception as e:
                    label.objects.filter(FK_coil_id=coilObj).delete()
                    coil.objects.filter(id=coilObj.id).delete()
                    msg = "Error al generar marbetes" + str(e)
            else:
                msg = 'Error al generar la bobina'
        else:
            msg = 'Ha ocurrido un error'
            print(form.errors)
    else:
        form = CreateCoilForm()
    if issaved:
        return redirect('/labelMenu/')

    return render(request, "cuervo/coil_create.html", {"form": form, "msg": msg})


def deleteLabelsOfaCoil(request, id):
    msg = None
    tittle = "Error al Eliminar Marbetes"
    link = "/coil"
    coilObj = coil.objects.get(id=id)
    num_form = coilObj.notDelivered
    if request.method == 'POST':
        DeleteFormEntry = formset_factory(DeleteLabelForm, extra=num_form)
        formset = DeleteFormEntry(request.POST)
        if formset.is_valid():
            for form in formset:
                uniqueid = form.cleaned_data.get('uniqueid')
                try:
                    label.objects.get(uniqueid=uniqueid, FK_coil_id=coilObj)
                except label.DoesNotExist:
                    msg = f"El marbete con el folio {uniqueid} no existe."
                    return render(request, "cuervo/display_error.html", {'tittle': tittle, "msg": msg, "link": link})
                label.objects.filter(uniqueid__contains=uniqueid, FK_coil_id=coilObj).delete()
            return redirect('/labelMenu/')
        else:
            msg = "Error"
    else:
        formset = formset_factory(DeleteLabelForm, extra=num_form)
    return render(request, 'cuervo/deleteLabelsOfaCoil.html', {'formset': formset, "msg": msg})





@permission_required('cuervo.add_coilstatus', login_url='/login/')
def Consumo_Envasado(request):
    msg = None
    orden = None
    bobinas = coil.objects.none()
    lotes_granel = granel_lot.objects.none()
    detalles_consumo = None
    form = None
    data_to_confirm = None
    confirmalert = 'none'
    progresomodal = 'none'

    try:
        if request.method == "POST":
            form = Consumo_Envform(request.POST)

            if 'buscar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    if orden.status == 'REL' or orden.status == 'CRTD':
                        lotes_granel = granel_lot.objects.filter(FK_order_id=orden)  # Filtra por orden
                        form.fields['granel_lot'].queryset = lotes_granel

                        detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)
                        print(detalles_consumo)


                    elif orden.status == 'TECO':
                        msg = 'Orden de producción cerrada'


                except order.DoesNotExist:
                    msg = 'Orden de producción no encontrada'

            if 'asignar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                granel_lot_id = request.POST.get("granel_lot")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)


                    # Obtener todas las bobinas de la orden
                    bobina_ids = [int(id) for id in orden.coils.split(',')]
                    bobinas = coil.objects.filter(id__in=bobina_ids).order_by('numrollo')

                    #lote_asignado = False   Variable para rastrear si algún lote fue asignado
                    lote_no_seleccionado = False  # Variable para rastrear si no se seleccionó lote
                    etiquetas_no_encontradas = True  # Variable para rastrear si no se encontraron etiquetas

                    folio_inicial = None
                    folio_final = None
                    cantidad_total = 0

                    for bobina in bobinas:
                        # Obtener todas las etiquetas "LEIDO" de la bobina
                        folios_leidos = label.objects.filter(FK_coil_id=bobina,
                                                             FK_labelStatus_id=labelStatus.objects.get(
                                                                 name='LEIDO')).values_list('uniqueid',
                                                                                            flat=True).order_by(
                            'uniqueid')
                        if folios_leidos:
                            etiquetas_no_encontradas = False  # Se encontraron etiquetas
                            if granel_lot_id:
                                lotgr = granel_lot.objects.get(id=granel_lot_id)
                                folios_list = list(folios_leidos)

                                

                                
                                if folio_inicial is None:
                                    folio_inicial = folios_list[0]  # Primer folio de la primera bobina

                                folio_final = folios_list[-1]  # Último folio de la última bobina
                                cantidad_total += len(folios_list)
                                ordenname = orden.uniqueid
                                granellotname = lotgr.granel_lot
                                
                            else:
                                lote_no_seleccionado = True  # Marcar que no se seleccionó un lote
                                break  # Salir del bucle si no se seleccionó un lote

                    if lote_no_seleccionado:
                        msg = 'Debe seleccionar un Lote'
                    elif etiquetas_no_encontradas:
                        msg = 'No hay marbetes escaneados para asignar'
                    else:
                        data_to_confirm = {
                            'folio_inicial': folio_inicial,
                            'folio_final': folio_final,
                            'cantidad': cantidad_total,
                            'lote_granel': granellotname,
                            'orden': ordenname,
                        }
                        confirmalert = 'block'
                    

                    lotes_granel = granel_lot.objects.filter(FK_order_id=orden)  # Filtra por orden
                    form.fields['granel_lot'].queryset = lotes_granel
                    detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)
                except (order.DoesNotExist, granel_lot.DoesNotExist):
                    msg = 'Orden de producción o Lote Granel no encontrado'
            if 'confirmar_asignacion' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                granel_lot_id = request.POST.get("granel_lot")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    # Obtener todas las bobinas de la orden
                    bobina_ids = [int(id) for id in orden.coils.split(',')]
                    bobinas = coil.objects.filter(id__in=bobina_ids).order_by('numrollo')

                    lote_asignado = False  # Variable para rastrear si algún lote fue asignado
                    lote_no_seleccionado = False  # Variable para rastrear si no se seleccionó lote
                    etiquetas_no_encontradas = True  # Variable para rastrear si no se encontraron etiquetas

                    confirmalert = 'none'
                    progresomodal = 'block'

                    for bobina in bobinas:
                        # Obtener todas las etiquetas "LEIDO" de la bobina
                        folios_leidos = label.objects.filter(FK_coil_id=bobina,
                                                             FK_labelStatus_id=labelStatus.objects.get(
                                                                 name='LEIDO')).values_list('uniqueid',
                                                                                            flat=True).order_by(
                            'uniqueid')
                        if folios_leidos:
                            etiquetas_no_encontradas = False  # Se encontraron etiquetas
                            if granel_lot_id:
                                folios_list = list(folios_leidos)
                                folio_inicial = folios_list[0]
                                folio_final = folios_list[-1]
                                cantidad = len(folios_list)
                                bobina_id = bobina.id
                                orden_id = orden.id
                            
                                if not GranelConsumptionDetail.objects.filter(
                                    FK_order_id=orden_id,
                                    FK_granel_lot_id=granel_lot_id,
                                    FK_coil_id=bobina_id,
                                    folio_inicial=folio_inicial,
                                    folio_final=folio_final,
                                    cantidad=cantidad
                                ).exists():
                                    GranelConsumptionDetail.objects.create(
                                        FK_order_id=orden_id,
                                        FK_granel_lot_id=granel_lot_id,
                                        FK_coil_id=bobina_id,
                                        folio_inicial=folio_inicial,
                                        folio_final=folio_final,
                                        cantidad=cantidad
                                    )
                                    lote_asignado = True  # Marcar que se asignó un lote
                                    # Actualizar el estado de las etiquetas a 'ASIGNADO'
                                    label.objects.filter(FK_coil_id=bobina, uniqueid__in=folios_list).update(
                                        FK_labelStatus_id=labelStatus.objects.get(name='Producido'))
                                else:
                                    lote_asignado = True  # Marcar que se asignó un lote
                            else:
                                lote_no_seleccionado = True  # Marcar que no se seleccionó un lote
                                break  # Salir del bucle si no se seleccionó un lote


                    if lote_no_seleccionado:
                        msg = 'Debe seleccionar un Lote'
                    elif lote_asignado:
                        msg = 'Lote asignado correctamente'
                    elif etiquetas_no_encontradas:
                        msg = 'No hay marbetes escaneados para asignar'

                    lotes_granel = granel_lot.objects.filter(FK_order_id=orden)  # Filtra por orden
                    form.fields['granel_lot'].queryset = lotes_granel
                    detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)
                    progresomodal = 'none'
                except (order.DoesNotExist, granel_lot.DoesNotExist):
                    msg = 'Orden de producción o Lote Granel no encontrado'

        else:
            form = Consumo_Envform()

        return render(request, "cuervo/consumo_env.html", {
            "form": form,
            "msg": msg,
            "orden": orden,
            "lotes_granel": lotes_granel,
            "detalles_consumo": detalles_consumo,
            "data_to_confirm": data_to_confirm,
            "confirmalert": confirmalert,
            "progresalert": progresomodal,
        })
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })




@permission_required('cuervo.view_granel_consumption_detail', login_url='/login/')
def Consumo_Manualidades(request):
    msg = None
    orden = None
    lotes_granel = granel_lot.objects.none()
    detalles_consumo = None
    form = None
    data_to_confirm = None
    confirmalert = 'none'
    progresomodal = 'none'

    print('entro 1')
    
    try:
        

        if request.method == "POST":

            print('entro post')
            form = Consumo_Manform(request.POST)

            if form.is_valid():
                print('form OK')

            else:
                print(form.errors)  # Imprime los errores del formulario

    
            if 'buscar' in request.POST and form.is_valid():
                print('entro')
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                print('entro', ordenproduccion)
    
                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)
                    print('entro', orden)
    
                    if orden.status == 'REL' or orden.status == 'CRTD':
                        lotes_granel = granel_lot.objects.filter(FK_order_id=orden)
                        print('entro', lotes_granel)
                        form.fields['granel_lot'].queryset = lotes_granel
    
                        detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)
    
    
                    elif orden.status == 'TECO':
                        msg = 'Orden de producción cerrada'
    
                except order.DoesNotExist:
                    msg = 'Orden de producción no encontrada'
    
            if 'asignar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                granel_lot_id = request.POST.get("granel_lot")
                folioinicial = form.cleaned_data.get("folioinicial")
                foliofinal = form.cleaned_data.get("foliofinal")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    # Filtrar las etiquetas en el rango de folios proporcionado
                    idmin = label.objects.filter(url=folioinicial).values_list('id', 'uniqueid').first()
                    idmax = label.objects.filter(url=foliofinal).values_list('id', 'uniqueid').first()

                    if idmin is None or idmax is None:
                        msg = 'No esta registrada una etiqueta escaneada'

                    idmin_val, uniqueidmin_val = idmin
                    idmax_val, uniqueidmax_val = idmax

                    etiquetas_rango = label.objects.filter(id__gte=idmin_val, id__lte=idmax_val).order_by('uniqueid')
                    # Actualizar el estado de las etiquetas a 'PRODUCIDO'
                    #etiquetas_rango.update(FK_labelStatus_id=labelStatus.objects.get(name='LEIDO'))

                    # Obtener todas las bobinas de la orden
                    bobina_ids = [int(id) for id in orden.coils.split(',')]

                    # Filtrar etiquetas en el rango de ids y que pertenezcan a las bobinas de la orden
                    etiquetas_rango = label.objects.filter(
                        id__gte=idmin_val,
                        id__lte=idmax_val,
                        FK_coil_id__in=bobina_ids  # Asegurar que las etiquetas pertenecen a las bobinas de la orden
                    ).order_by('uniqueid')

                    lote_no_seleccionado = False  # Variable para rastrear si no se seleccionó lote
                    etiquetas_no_encontradas = not etiquetas_rango.exists()  # Variable para rastrear si no se encontraron etiquetas

                    if etiquetas_no_encontradas:
                        msg = 'No hay marbetes escaneados para asignar'
                    else:
                        folios_list = list(etiquetas_rango.values_list('uniqueid', flat=True))

                        # Obtener el folio inicial y final
                        folio_inicial = folios_list[0]  # Primer folio en el rango
                        folio_final = folios_list[-1]  # Último folio en el rango
                        cantidad_total = len(folios_list)  # Contar el número de folios en el rango

                        if granel_lot_id:
                            lotgr = granel_lot.objects.get(id=granel_lot_id)
                            granellotname = lotgr.granel_lot
                            ordenname = orden.uniqueid

                            data_to_confirm = {
                                'folio_inicial': folio_inicial,
                                'folio_final': folio_final,
                                'cantidad': cantidad_total,
                                'lote_granel': granellotname,
                                'orden': ordenname,
                            }
                            confirmalert = 'block'
                        else:
                            lote_no_seleccionado = True

                    if lote_no_seleccionado:
                        msg = 'Debe seleccionar un Lote'

                    # Actualizar el queryset de los lotes granel en el formulario
                    lotes_granel = granel_lot.objects.filter(FK_order_id=orden)  # Filtrar por orden
                    form.fields['granel_lot'].queryset = lotes_granel
                    detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)

                except (order.DoesNotExist, granel_lot.DoesNotExist):
                    msg = 'Orden de producción o Lote Granel no encontrado'
            if 'confirmar_asignacion' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                granel_lot_id = request.POST.get("granel_lot")
                folioinicial = form.cleaned_data.get("folioinicial")
                foliofinal = form.cleaned_data.get("foliofinal")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    # Filtrar las etiquetas en el rango de folios proporcionado
                    idmin = label.objects.filter(url=folioinicial).values_list('id', 'uniqueid').first()
                    idmax = label.objects.filter(url=foliofinal).values_list('id', 'uniqueid').first()

                    confirmalert = 'none'
                    progresomodal = 'block'

                    if idmin is None or idmax is None:
                        msg = 'No esta registrada una etiqueta escaneada'
                    else:
                        idmin_val, uniqueidmin_val = idmin
                        idmax_val, uniqueidmax_val = idmax

                        # Obtener todas las bobinas de la orden
                        bobina_ids = [int(id) for id in orden.coils.split(',')]

                        # Filtrar etiquetas en el rango de ids y que pertenezcan a las bobinas de la orden
                        etiquetas_rango = label.objects.filter(
                            id__gte=idmin_val,
                            id__lte=idmax_val,
                            FK_coil_id__in=bobina_ids  # Asegurar que las etiquetas pertenecen a las bobinas de la orden
                        ).order_by('uniqueid')

                        if etiquetas_rango:
                            # Actualizar el estado de las etiquetas a 'PRODUCIDO'
                            etiquetas_rango.update(FK_labelStatus_id=labelStatus.objects.get(name='LEIDO'))

                            bobinas = coil.objects.filter(id__in=bobina_ids).order_by('numrollo')

                            lote_asignado = False  # Variable para rastrear si algún lote fue asignado
                            lote_no_seleccionado = False  # Variable para rastrear si no se seleccionó lote
                            etiquetas_no_encontradas = True  # Variable para rastrear si no se encontraron etiquetas



                            for bobina in bobinas:
                                # Obtener todas las etiquetas "LEIDO" de la bobina
                                folios_leidos = label.objects.filter(FK_coil_id=bobina,
                                                                     FK_labelStatus_id=labelStatus.objects.get(
                                                                         name='LEIDO')).values_list('uniqueid',
                                                                                                    flat=True).order_by(
                                    'uniqueid')
                                if folios_leidos:
                                    etiquetas_no_encontradas = False  # Se encontraron etiquetas
                                    if granel_lot_id:
                                        folios_list = list(folios_leidos)
                                        folio_inicial = folios_list[0]
                                        folio_final = folios_list[-1]
                                        cantidad = len(folios_list)
                                        bobina_id = bobina.id
                                        orden_id = orden.id

                                        if not GranelConsumptionDetail.objects.filter(
                                                FK_order_id=orden_id,
                                                FK_granel_lot_id=granel_lot_id,
                                                FK_coil_id=bobina_id,
                                                folio_inicial=folio_inicial,
                                                folio_final=folio_final,
                                                cantidad=cantidad
                                        ).exists():
                                            GranelConsumptionDetail.objects.create(
                                                FK_order_id=orden_id,
                                                FK_granel_lot_id=granel_lot_id,
                                                FK_coil_id=bobina_id,
                                                folio_inicial=folio_inicial,
                                                folio_final=folio_final,
                                                cantidad=cantidad
                                            )
                                            lote_asignado = True  # Marcar que se asignó un lote
                                            # Actualizar el estado de las etiquetas a 'ASIGNADO'
                                            label.objects.filter(FK_coil_id=bobina, uniqueid__in=folios_list).update(
                                                FK_labelStatus_id=labelStatus.objects.get(name='Producido'))
                                        else:
                                            lote_asignado = True  # Marcar que se asignó un lote
                                    else:
                                        lote_no_seleccionado = True  # Marcar que no se seleccionó un lote
                                        break  # Salir del bucle si no se seleccionó un lote

                            if lote_no_seleccionado:
                                msg = 'Debe seleccionar un Lote'
                            elif lote_asignado:
                                msg = 'Lote asignado correctamente'
                            elif etiquetas_no_encontradas:
                                msg = 'No hay marbetes escaneados para asignar'

                            lotes_granel = granel_lot.objects.filter(FK_order_id=orden)  # Filtra por orden
                            form.fields['granel_lot'].queryset = lotes_granel
                            detalles_consumo = GranelConsumptionDetail.objects.filter(FK_order_id=orden)
                            progresomodal = 'none'
                        else:
                            msg = 'No se logro encontrar marbetes dentro del rango'

                except (order.DoesNotExist, granel_lot.DoesNotExist):
                    msg = 'Orden de producción o Lote Granel no encontrado'
    
        else:
            form = Consumo_Manform()
    
        return render(request, "cuervo/consumo_man.html", {
            "form": form,
            "msg": msg,
            "orden": orden,
            "lotes_granel": lotes_granel,
            "detalles_consumo": detalles_consumo,
            "data_to_confirm": data_to_confirm,
            "confirmalert": confirmalert,
            "progresalert": progresomodal,
        })
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })

def transformar_lote(numero):
    # Convertir el número a string en caso de ser un entero
    numero_str = str(numero)
    
    # El año está en las posiciones -4 y -3 (ejemplo: "24" en "1908324051")
    año = numero_str[-5:-3]
    
    # El número de lote está en las posiciones -3, -2 y -1 (ejemplo: "051" en "1908324051")
    lote = numero_str[-3:]
    
    # Armar el nuevo formato L<lote><año>
    nuevo_lote = f"L{lote}{año}"
    
    return nuevo_lote

@permission_required('cuervo.add_coilstatus', login_url='/login/')
def init_granel_lot(request):
    msg = None
    orden = None
    lotes_granel = granel_lot.objects.none()

    try:
        if request.method == "POST":
            form = AddGranelloteform(request.POST)

            if 'buscar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    if orden.status == 'REL' or orden.status == 'CRTD':
                        lotes_granel = granel_lot.objects.filter(FK_order_id=orden)


                    elif orden.status == 'TECO':
                        msg = 'Orden de producción cerrada'


                except order.DoesNotExist:
                    msg = 'Orden de producción no encontrada'

            if 'asignar' in request.POST and form.is_valid():
                ordenproduccion = form.cleaned_data.get("ordenproduccion")
                granellot = form.cleaned_data.get("granel_lot")

                try:
                    orden = order.objects.get(uniqueid=ordenproduccion)

                    if granellot:
                        # Transformar el lote ingresado con la nueva función
                        lote_transformado = transformar_lote(granellot)
                        # Verificar si el lote ya existe para la misma orden
                        if not granel_lot.objects.filter(granel_lot=lote_transformado, FK_order_id=orden.id).exists():
                            granel_lot.objects.create(
                                granel_lot=lote_transformado,
                                FK_order_id=orden
                            )
                            msg = 'Lote Granel creado correctamente'
                        else:
                            msg = 'El Lote Granel ya existe para esta orden de producción'
                    else:
                        msg = 'No hay Lote para asignar'

                    lotes_granel = granel_lot.objects.filter(FK_order_id=orden)
                except (order.DoesNotExist):
                    msg = 'Orden de producción no encontrada'

        else:
            form = AddGranelloteform()

        return render(request, "cuervo/lote_granel.html", {
            "form": form,
            "msg": msg,
            "orden": orden,
            "lotes_granel": lotes_granel,
        })
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })



def delete_granel_lot(request, pk):
    try:
        granel_lot_instance = get_object_or_404(granel_lot, pk=pk)
        granel_lot_instance.delete()
        return redirect(reverse('granel-lote'))
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })


@permission_required('cuervo.add_coilstatus', login_url='/login/')
def num_asignacion(request):
    msg = None
    sku = None

    try:
        if request.method == "POST":
            form = NumAsignacionform(request.POST)

            if 'buscar' in request.POST and form.is_valid():
                skusearch = form.cleaned_data.get("sku")

                try:
                    sku = SKU.objects.get(sku=skusearch)
                except SKU.DoesNotExist:
                    msg = "El SKU no existe."

            if 'asignar' in request.POST and form.is_valid():
                skusearch = form.cleaned_data.get("sku")
                noasignacion = form.cleaned_data.get("noasignacion")

                try:
                    sku = SKU.objects.get(sku=skusearch)
                    if sku.asignacion:
                        sku.asignacion = noasignacion
                        msg = "Número de asignación actualizado."
                    else:
                        sku.asignacion = noasignacion
                        msg = "Número de asignación asignado."
                    sku.save()

                except SKU.DoesNotExist:
                    msg = "El SKU no existe y no se puede asignar el número."

        else:
            form = NumAsignacionform()

        return render(request, "cuervo/no_asignacion.html", {
            "form": form,
            "msg": msg,
            "sku": sku
        })
    except Exception as e:
        msg = f'Ocurrió un error: {str(e)}'
        return render(request, "cuervo/ErrorMsg.html", {
            "msg": msg
        })






