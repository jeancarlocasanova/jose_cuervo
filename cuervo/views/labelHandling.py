from django.shortcuts import render, redirect, get_object_or_404, reverse
from ..models import label, coil, labelStatus, init_label, order, lot, coilStatus, coil_request, \
    coil_request_status, coilType, inventoryLocation, granel_lot
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from ..form import FilterLabelForm, UpdateLabelForm, LabelInitForm, CreateCoilFormv2
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import csv
from datetime import datetime
from django.contrib import messages
from openpyxl import load_workbook
import re
from django.utils import timezone
from django.http import HttpResponse

def labelHandling_view(request):
    if request.method == 'POST':
        labelList = None
        form = FilterLabelForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data['uniqueid']
            coil = form.cleaned_data['coil']
            if uniqueid:
                labelList = label.objects.filter(uniqueid__contains=uniqueid)
            if coil:
                labelList = label.objects.filter(FK_coil_id=coil)
            return render(request, "cuervo/labelHandling.html", {'labelList': labelList})
    else:
        form = FilterLabelForm()
    return render(request, 'cuervo/labelFilterForm.html', {'form': form})

class updateLabel_view(PermissionRequiredMixin, UpdateView):
    model = label
    template_name = 'cuervo/label_edit.html'
    success_url = reverse_lazy('labelHandling')
    form_class = UpdateLabelForm
    permission_required = 'cuervo.change_label'

#<----------------------- Search Label By Coil ID -------------------------------->
def searchLabelByCoilFK(request, pk):
    coilFk = get_object_or_404(coil, id=pk)
    labels = label.objects.filter(FK_coil_id=coilFk)
    coil_not_delivered = coilFk.notDelivered

    if request.method == 'POST':
        selected_labels = request.POST.getlist('selected_labels')
        faltante = request.POST.get('faltante', 'off')

        selected_labels_count = len(selected_labels)
        faltante_labels_count = labels.filter(FK_labelStatus_id__name='Faltante').count()

        if faltante == 'on':
            faltante_labels_count += selected_labels_count

        if faltante_labels_count <= coil_not_delivered:
            for label_id in selected_labels:
                label_obj = label.objects.get(id=label_id)
                if faltante == 'on':
                    label_obj.FK_labelStatus_id = labelStatus.objects.get(name='Faltante')
                else:
                    label_obj.FK_labelStatus_id = labelStatus.objects.get(name='Faltante')  # Define your other status
                label_obj.save()

        # Redirect to the same page to avoid form resubmission
        return redirect('label-find', pk=pk)

    total_labels = labels.count()
    faltante_labels = labels.filter(FK_labelStatus_id__name='Faltante').count()

    disable_checkboxes = faltante_labels >= coil_not_delivered

    return render(request, 'cuervo/label_by_CoilFk.html', {
        'labels': labels,
        'disable_checkboxes': disable_checkboxes,
    })

#-------------------- Init Label  ------------------------------


@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_information(request):
        msg = None
        issaved = None
        if request.method == "POST":
            form = LabelInitForm(request.POST)
            if form.is_valid():
                csv_files = request.FILES.getlist('csv_file')
                brand = form.cleaned_data.get('brand')
                supplier = form.cleaned_data.get('supplier')
                # Obtener la fecha actual
                fecha_actual = datetime.now()

                # Sumar nueve meses a la fecha actual
                anno = fecha_actual.year + (fecha_actual.month + 9) // 12
                mes = (fecha_actual.month + 9) % 12
                if mes == 0:
                    mes = 12
                dia = min(fecha_actual.day, [31,
                                             29 if anno % 4 == 0 and (anno % 100 != 0 or anno % 400 == 0) else 28,
                                             31, 30, 31, 30, 31, 31, 30, 31, 30, 31][mes - 1])

                fecha_nueve_meses_despues = datetime(anno, mes, dia)
                ministrationNumber = form.cleaned_data.get('ministrationNumber')
                for csv_file in csv_files:
                    if not csv_file.name.endswith('.csv'):
                        # Handle error: Invalid file format for a specific file
                        continue  # Skip this file and move to the next one

                    # Columnas a excluir (ID y Registro en este caso)
                    columns_to_exclude = ['ID', 'REGISTRO']

                    folios = []
                    textos = []

                    decoded_file = csv_file.read().decode('utf-8')
                    csv_reader = csv.reader(decoded_file.splitlines(), delimiter=',')

                    # Obtiene los encabezados del archivo CSV
                    headers = next(csv_reader)

                    # Encuentra los índices de las columnas a excluir
                    exclude_indices = [headers.index(column) for column in columns_to_exclude if column in headers]

                    for row in csv_reader:
                        # Excluye las columnas en cada fila
                        filtered_row = [value for index, value in enumerate(row) if index not in exclude_indices]
                        # Divide los folios y los textos en arreglos separados
                        folios.extend(filtered_row[::2])  # Obtén los folios (columnas pares)
                        textos.extend(filtered_row[1::2])  # Obtén los textos (columnas impares)

                    # Verifica si hay contenido repetido en los textos
                    duplicates = []
                    seen = set()
                    for i, texto in enumerate(textos):
                        if texto in seen:
                            duplicates.append(i)
                        else:
                            seen.add(texto)

                    folios_filtrado = [valor for valor in folios if not valor.isdigit()]
                    if (textos != []) and folios_filtrado != [] and not duplicates:
                        data_exists = label.objects.filter(uniqueid__in=textos, url__in=folios_filtrado)
                        folios_filtrado = [valor for valor in folios_filtrado if valor.strip()]
                        if not data_exists:
                            try:
                                if len(folios_filtrado) == len(textos):
                                    for index, x in enumerate(folios_filtrado):
                                         init_label.objects.create(
                                            uniqueid=folios_filtrado[index],
                                            url=textos[index],
                                            file_name=str(csv_file.name),
                                            brand=brand,
                                            ministrationNumber=ministrationNumber,
                                            supplier=supplier,
                                            expiration=fecha_nueve_meses_despues
                                         ).save()
                            except Exception as e:
                                #label.objects.filter(FK_coil_id=coilObj).delete()
                                msg = "Error al generar marbetes" + str(e)
                        else:
                            msg = "Algunos de estos marbetes ya existen"
                    else:
                        if duplicates:
                            # Aquí puedes trabajar con los datos repetidos
                            for index in duplicates:
                                print(f"El texto '{textos[index]}' está repetido en el folio: {folios[index]}.")
                        else:
                            msg = 'Revisa si los números de folio o los folios no entregados estén bien'
                issaved = True
            else:
                msg = 'Ha ocurrido un error'
                print(form.errors)
        else:
            form = LabelInitForm()
        if issaved:
            return redirect('/labelMenu/')

        return render(request, "cuervo/label_init_create.html", {"form": form, "msg": msg})


def extract_data_from_excel_No_Rollo(file, sheet_name_pattern):
    values = []
    # Load the Excel workbook
    wb = load_workbook(file)

    # Find the worksheet that matches the pattern
    matching_sheets = [ws for ws in wb.sheetnames if re.search(sheet_name_pattern, ws, re.IGNORECASE)]
    if not matching_sheets:
        raise ValueError("No sheet found matching the pattern: {}".format(sheet_name_pattern))

    ws = wb[matching_sheets[0]]
    row = ws.max_row
    for i in range(2, row + 1):
        cell_value = ws.cell(row=i, column=1).value
        if cell_value is not None:
            values.append(cell_value)
        else:
            break  # Stop loop if encountering a None value

    return values

def extract_data_from_excel_folios(file, sheet_name_pattern):
    values = []
    # Load the Excel workbook
    wb = load_workbook(file)

    # Find the worksheet that matches the pattern
    matching_sheets = [ws for ws in wb.sheetnames if re.search(sheet_name_pattern, ws, re.IGNORECASE)]
    if not matching_sheets:
        raise ValueError("No sheet found matching the pattern: {}".format(sheet_name_pattern))

    ws = wb[matching_sheets[0]]
    row = ws.max_row
    #print(ws['A1'].value)
    for i in range(2, row + 1):
        cell_value = ws.cell(row=i, column=2).value
        if cell_value is not None:
            values.append(cell_value)
        else:
            break  # Stop loop if encountering a None value

    return values

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_canceled(request):
        msg = None
        issaved = None
        if request.method == "POST":
            csv_files = request.FILES.getlist('csv_file')
            for file in csv_files:
                sheet_name = 'folios con defecto'
                # Extract data from the specified cell
                valueNoRollo = extract_data_from_excel_No_Rollo(file, sheet_name)
                valueFolios = extract_data_from_excel_folios(file, sheet_name)

        if issaved:
            return redirect('/labelMenu/')

        return render(request, "cuervo/label_canceled.html", {"msg": msg})

codigos_escaneados = []
@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_damaged(request):
    return render(request, "cuervo/label_damaged.html", {'codigos': codigos_escaneados})

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def agregar_codigo(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        codigos_escaneados.append(codigo)  # Agregar el código a la lista interna
    return redirect('label-damaged')

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def confirmar_listado(request):
    codigos_input = request.POST.get('codigos', '')  # Obtener los códigos del campo oculto
    codigos_escaneados.extend(codigos_input.split(','))  # Agregar los códigos a la lista interna
    codigos_bd = label.objects.values_list('uniqueid', flat=True)

    codigos_no_cambiados = []  # Lista para almacenar los códigos que no se cambiaron de estado

    for codigo in codigos_escaneados:
        if codigo in codigos_bd:
            # Verificar si el código ya está registrado como dañado
            if not label.objects.filter(uniqueid=codigo, FK_labelStatus_id__name="dañado").exists():
                # Actualizar el estado a "dañado" en la base de datos
                codigo_obj = label.objects.get(uniqueid=codigo)
                labelStatus_obj = labelStatus.objects.get(name="dañado")
                codigo_obj.FK_labelStatus_id = labelStatus_obj
                codigo_obj.save()
            else:
                codigos_no_cambiados.append(codigo)  # Agregar el código a la lista de no cambiados
        else:
            codigos_no_cambiados.append(codigo)  # Agregar el código a la lista de no cambiados

    # Limpiar la lista de códigos escaneados
    codigos_escaneados.clear()

    # Mensaje de alerta para los códigos no cambiados
    if codigos_no_cambiados:
        messages.warning(request, f"Los siguientes códigos no se cambiaron de estado: {', '.join(codigos_no_cambiados)}")

    return redirect('label-damaged')

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def quitar_codigo(request, codigo):
    if codigo in codigos_escaneados:
        codigos_escaneados.remove(codigo)  # Remover el código de la lista interna
    return redirect('label-damaged')




@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_coil_create(request):
    msg = None
    orden = None
    selected_lote = None
    selected_lote_id = None
    selected_granel_lote = None
    selected_granel_lote_id = None
    lotes = []
    granel_lotes = []
    bobinas_disponibles = []
    bobinas = []
    selected_order_coils = []

    if request.method == "POST":
        form = CreateCoilFormv2(request.POST)

        if 'buscar' in request.POST and form.is_valid():
            ordenproduccion = form.cleaned_data.get("ordenproduccion")
            try:
                orden = order.objects.get(uniqueid=ordenproduccion)
                lotes = lot.objects.filter(FK_order_id=orden)
                granel_lotes = granel_lot.objects.filter(FK_order_id=orden)

                selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                bobinas = coil.objects.filter(
                    sku=orden.FK_sku_id.description
                ).exclude(
                    FK_coilStatus_id=coilStatus.objects.get(name='Asignada')
                ) | coil.objects.filter(
                    id__in=[int(id) for id in selected_order_coils]
                )

            except order.DoesNotExist:
                msg = 'Orden de producción no encontrada'

        elif 'crear' in request.POST and form.is_valid():
            bobinas_seleccionadas_str = request.POST.get('current_bobinas', '')
            bobinas_seleccionadas = [int(id) for id in bobinas_seleccionadas_str.split(',') if id.isdigit()]

            initial_bobinas_str = request.POST.get('initial_bobinas', '')
            initial_bobinas = [int(id) for id in initial_bobinas_str.split(',') if id.isdigit()]

            ordenproduccion = form.cleaned_data.get("ordenproduccion")
            orden = order.objects.get(uniqueid=ordenproduccion)
            if not orden:
                msg = 'Orden de producción no seleccionada.'
            else:
                bobinas_a_desasignar = list(set(initial_bobinas) - set(bobinas_seleccionadas))
                bobinas_a_asignar = list(set(bobinas_seleccionadas) - set(initial_bobinas))

                for bobina_id in bobinas_a_desasignar:
                    bobina = coil.objects.get(id=bobina_id)
                    bobina.FK_coilStatus_id = coilStatus.objects.get(name='Sin asignar')
                    bobina.save()

                for bobina_id in bobinas_a_asignar:
                    bobina = coil.objects.get(id=bobina_id)
                    bobina.FK_coilStatus_id = coilStatus.objects.get(name='Asignada')
                    bobina.save()

                bobinas_actualizadas = sorted(bobinas_seleccionadas)
                orden.coils = ','.join(map(str, bobinas_actualizadas))
                orden.save()
                msg = 'Bobinas actualizadas con éxito en la orden.'

        elif 'selected_lote' in request.POST:
            selected_lote_id = request.POST.get('selected_lote')
            if selected_lote_id:
                try:
                    selected_lote = lot.objects.get(id=selected_lote_id)
                    if not orden:
                        orden = selected_lote.FK_order_id
                        lotes = lot.objects.filter(FK_order_id=orden)
                        granel_lotes = granel_lot.objects.filter(FK_order_id=orden)

                        selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                        bobinas = coil.objects.filter(
                            sku=orden.FK_sku_id.description
                        ).exclude(
                            FK_coilStatus_id=coilStatus.objects.get(name='Asignada')
                        ) | coil.objects.filter(
                            id__in=[int(id) for id in selected_order_coils]
                        )

                except lot.DoesNotExist:
                    selected_lote = None

    else:
        form = CreateCoilFormv2()

    return render(request, "cuervo/coil_createv2.html", {
        "form": form,
        "msg": msg,
        "bobinas": bobinas,
        "orden": orden,
        "lotes": lotes if orden else [],
        "granel_lotes": granel_lotes if orden else [],
        "selected_lote": selected_lote,
        "selected_lote_id": selected_lote_id,
        "selected_granel_lote": selected_granel_lote,
        "selected_granel_lote_id": selected_granel_lote_id,
        "selected_order_coils": selected_order_coils,
    })

def extract_data_from_excel_warehouse_label(file, sheet_name_pattern):
    values = {}
    no_rollo = []
    folios_iniciales = []
    folios_finales = []
    folios_utilizados = []
    folios_faltantes = []
    cantidad_rollo = []
    num_caja = []
    cantidad_caja = []

    # Load the Excel workbook with data_only=True
    wb = load_workbook(file, data_only=True)

    # Find the worksheet that matches the pattern
    matching_sheets = [ws for ws in wb.sheetnames if re.search(sheet_name_pattern, ws, re.IGNORECASE)]
    if not matching_sheets:
        raise ValueError("No sheet found matching the pattern: {}".format(sheet_name_pattern))

    ws = wb[matching_sheets[0]]

    values['proveedor'] = ws['B4'].value
    values['ot'] = ws['B7'].value
    values['etiqueta'] = ws['B8'].value
    values['item'] = ws['B9'].value

    values['orden'] = ws['D7'].value
    values['desc'] = ws['D8'].value
    values['factura'] = ws['D9'].value

    # Iterate over rows starting from row 13
    for row in ws.iter_rows(min_row=13, min_col=1, max_col=8, values_only=True):
        if any(cell is None for cell in row):
            break
        no_rollo.append(row[0])
        folios_iniciales.append(row[1])
        folios_finales.append(row[2])
        folios_utilizados.append(row[3])
        folios_faltantes.append(row[4])
        cantidad_rollo.append(row[5])
        num_caja.append(row[6])
        cantidad_caja.append(row[7])

    values['folios_iniciales'] = folios_iniciales
    values['folios_finales'] = folios_finales
    values['folios_utilizados'] = folios_utilizados
    values['folios_faltantes'] = folios_faltantes
    values['cantidad_rollo'] = cantidad_rollo
    values['num_caja'] = num_caja
    values['cantidad_caja'] = cantidad_caja
    values['num_rollo'] = no_rollo

    return values
@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_in_inventory(request):
    msg = None
    if request.method == "POST":
        csv_files = request.FILES.getlist('csv_file')
        obj_status = coilStatus.objects.get(name='Disponible').first()
        obj_type = coilType.objects.all().first()
        obj_label_status = labelStatus.objects.get(name='Asignado').first()
        obj_inventory = inventoryLocation.objects.get(name='Almacen').first()
        try:
            for file in csv_files:
                sheet_name = 'OT'
                # Extract data from the specified cell
                labels = extract_data_from_excel_warehouse_label(file, sheet_name)
                if not labels:
                    messages.error(request, 'No se encontraron datos válidos en el archivo.')
                    continue
                for i in range(len(labels['folios_iniciales'])):
                    if labels['folios_iniciales'][i] is None or labels['folios_finales'][i] is None:
                        messages.error(request, 'Faltan datos esenciales para crear el objeto coil.')
                        continue
                    obj_coil = coil.objects.create(
                        initNumber=labels['folios_iniciales'][i],
                        finishNumber=labels['folios_finales'][i],
                        numrollo=labels['num_rollo'][i],
                        notDelivered=labels['folios_faltantes'][i],
                        missing=labels['cantidad_rollo'][i],
                        delivered=labels['folios_utilizados'][i],
                        boxNumber=labels['num_caja'][i],
                        purchaseOrder=labels['orden'],
                        orderUniqueid=labels['ot'],
                        sku=labels['desc'],
                        FK_coilStatus_id=obj_status,
                        FK_coilType_id=obj_type,
                        last_edit_user=request.user
                    )
                    matching_labels = init_label.objects.filter(
                        uniqueid__gte=labels['folios_iniciales'][i],
                        uniqueid__lte=labels['folios_finales'][i]
                    )
                    for matching_label in matching_labels:
                        label.objects.create(
                            uniqueid=matching_label.uniqueid,
                            url=matching_label.url,
                            brand=matching_label.brand,
                            ministrationNumber=matching_label.ministrationNumber,
                            supplier=matching_label.supplier,
                            FK_coil_id=obj_coil,
                            FK_labelStatus_id=obj_label_status,
                            FK_inventoryLocation_id=obj_inventory,
                            last_edit_user=request.user,
                            expiration=matching_label.expiration
                        )
            msg = "Datos cargados exitosamente."
        except Exception as e:
            messages.error(request, f'Hubo un error al cargar datos: {str(e)}')
    return render(request, "cuervo/label_in_inventory.html", {"msg": msg})


def view_coils(request, pk):
    solicitud = coil_request.objects.get(pk=pk)
    bobinas_ids = [int(id) for id in solicitud.requested_coils.split(',')]  # Obtener los IDs de las bobinas
    bobinas = coil.objects.filter(id__in=bobinas_ids)  # Obtener las instancias de las bobinas
    return render(request, 'cuervo/view_coils.html', {'solicitud': solicitud, 'bobinas': bobinas})

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def solicitudmarbete_request(request, pk):
    msg = None
    orden = None
    bobinas = []
    selected_lote_coils = []
    marbetes_necesarios = 0

    coil_request_instance = get_object_or_404(coil_request, pk=pk)

    if request.method == "POST":
        form = CreateCoilFormv2(request.POST)

        if 'crear' in request.POST and form.is_valid():
            bobinas_seleccionadas = request.POST.getlist('selected_bobinas')

            if not bobinas_seleccionadas:
                msg = 'Debe seleccionar al menos una bobina para actualizar la solicitud.'
            else:
                total_quantity = sum(
                    int(coil.numrollo) for coil in coil.objects.filter(id__in=bobinas_seleccionadas))

                # Guardar la orden para asegurarse de que no quede en null
                if not orden:
                    orden = coil_request_instance.FK_order_id


                # Obtener las bobinas previamente seleccionadas
                previously_selected_coils = [int(id) for id in coil_request_instance.requested_coils.split(',')] if coil_request_instance.requested_coils else []

                coil_request_instance.FK_order_id = orden
                coil_request_instance.requested_coils = ','.join(bobinas_seleccionadas)
                coil_request_instance.request_date = timezone.now()
                coil_request_instance.FK_coil_request_status_id = coil_request_status.objects.get(
                    status='Pendiente')
                coil_request_instance.created_by = request.user
                coil_request_instance.total_number = total_quantity
                coil_request_instance.save()

                # Cambiar el estado de las bobinas seleccionadas
                coil.objects.filter(id__in=bobinas_seleccionadas).update(
                    FK_coilStatus_id=coilStatus.objects.get(name__in='Solicitada')
                )

                # Cambiar el estado de las bobinas desmarcadas (las que estaban seleccionadas pero ya no lo están) a 'Asignada'
                bobinas_deseleccionadas = set(previously_selected_coils) - set(map(int, bobinas_seleccionadas))
                if bobinas_deseleccionadas:
                    coil.objects.filter(id__in=bobinas_deseleccionadas).update(
                        FK_coilStatus_id=coilStatus.objects.get(name__in='Asignada')
                    )

                # Devolver una respuesta con JavaScript
                return HttpResponse("""
                                <script>
                                    alert('La solicitud se ha actualizado correctamente.');
                                    window.location.href = '/coil-request/';
                                </script>
                            """)

        elif 'seleccionar' in request.POST and form.is_valid():
            marbetes_necesarios = int(request.POST.get('marbetes_necesarios', 0))
            try:
                orden = coil_request_instance.FK_order_id
                selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []

                assigned_coil_ids = coil_request.objects.exclude(pk=pk).values_list('requested_coils', flat=True)
                assigned_coil_ids = [int(id) for sublist in assigned_coil_ids for id in sublist.split(',') if id]

                bobinas = coil.objects.filter(
                    id__in=selected_order_coils,
                    FK_coilStatus_id=coilStatus.objects.get(name='Asignada')
                ).exclude(id__in=assigned_coil_ids)

                total_marbetes = 0
                selected_bobinas_ids = []
                for bobina in bobinas:
                    if total_marbetes < marbetes_necesarios:
                        total_marbetes += bobina.numrollo
                        selected_bobinas_ids.append(bobina.id)

                for bobina in bobinas:
                    bobina.selected = bobina.id in selected_bobinas_ids

                previously_selected_coils = [int(id) for id in coil_request_instance.requested_coils.split(
                    ',')] if coil_request_instance.requested_coils else []
                selected_lote_coils = [bobina.id for bobina in
                                       bobinas.filter(id__in=selected_bobinas_ids + previously_selected_coils)]

                # Render the template with the updated selection
                return render(request, "cuervo/solicitudmarbete.html", {
                    "form": form,
                    "msg": msg,
                    "bobinas": bobinas,
                    "orden": orden,
                    "selected_lote_coils": selected_lote_coils,
                    "coil_request_instance": coil_request_instance,
                    "marbetes_necesarios": marbetes_necesarios
                })

            except order.DoesNotExist:
                msg = 'Orden de producción no encontrada'
            except lot.DoesNotExist:
                msg = 'Lote granel no encontrado'
    else:
        if coil_request_instance.FK_order_id:
            orden = coil_request_instance.FK_order_id

        form = CreateCoilFormv2(initial={'ordenproduccion': coil_request_instance.FK_order_id.uniqueid})

        if orden:
            # Obtener todas las bobinas de la orden
            all_coils_in_order = coil.objects.filter(
                id__in=[int(id) for id in orden.coils.split(',')] if orden.coils else []
            )

            # Obtener bobinas asignadas a otras solicitudes
            assigned_coil_ids = coil_request.objects.exclude(pk=pk).values_list('requested_coils', flat=True)
            assigned_coil_ids = [int(id) for sublist in assigned_coil_ids for id in sublist.split(',') if id]

            # Excluir las bobinas asignadas a otras solicitudes
            bobinas = all_coils_in_order.exclude(id__in=assigned_coil_ids)

            # Obtener bobinas asignadas a esta solicitud específica
            selected_coil_ids = [int(id) for id in coil_request_instance.requested_coils.split(
                ',')] if coil_request_instance.requested_coils else []
            selected_lote_coils = [bobina.id for bobina in all_coils_in_order.filter(id__in=selected_coil_ids)]

        return render(request, "cuervo/solicitudmarbete.html", {
            "form": form,
            "msg": msg,
            "bobinas": bobinas,
            "orden": orden,
            "selected_lote_coils": selected_lote_coils,  # Lista de IDs de bobinas seleccionadas
            "coil_request_instance": coil_request_instance,
        })

codigos_escaneados = []
@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_damaged(request):
    return render(request, "cuervo/label_damaged.html", {'codigos': codigos_escaneados})

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def agregar_codigo(request):
    if request.method == 'POST':
        codigo = request.POST['codigo']
        codigos_escaneados.append(codigo)  # Agregar el código a la lista interna
    return redirect('label-damaged')

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def confirmar_listado(request):
    codigos_input = request.POST.get('codigos', '')  # Obtener los códigos del campo oculto
    codigos_escaneados.extend(codigos_input.split(','))  # Agregar los códigos a la lista interna
    codigos_bd = label.objects.values_list('uniqueid', flat=True)

    codigos_no_cambiados = []  # Lista para almacenar los códigos que no se cambiaron de estado

    for codigo in codigos_escaneados:
        if codigo in codigos_bd:
            # Verificar si el código ya está registrado como dañado
            if not label.objects.filter(uniqueid=codigo, FK_labelStatus_id__name="dañado").exists():
                # Actualizar el estado a "dañado" en la base de datos
                codigo_obj = label.objects.get(uniqueid=codigo)
                labelStatus_obj = labelStatus.objects.get(name="dañado")
                codigo_obj.FK_labelStatus_id = labelStatus_obj
                codigo_obj.save()
            else:
                codigos_no_cambiados.append(codigo)  # Agregar el código a la lista de no cambiados
        else:
            codigos_no_cambiados.append(codigo)  # Agregar el código a la lista de no cambiados

    # Limpiar la lista de códigos escaneados
    codigos_escaneados.clear()

    # Mensaje de alerta para los códigos no cambiados
    if codigos_no_cambiados:
        messages.warning(request, f"Los siguientes códigos no se cambiaron de estado: {', '.join(codigos_no_cambiados)}")

    return redirect('label-damaged')

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def quitar_codigo(request, codigo):
    if codigo in codigos_escaneados:
        codigos_escaneados.remove(codigo)  # Remover el código de la lista interna
    return redirect('label-damaged')

@permission_required('cuervo.delete_coil_request', login_url='/login/')
def delete_coil_request(request, pk):
    coil_request_instance = get_object_or_404(coil_request, pk=pk)

    # Obtener las bobinas asociadas a la solicitud
    requested_coils_ids = [int(id) for id in coil_request_instance.requested_coils.split(',')] if coil_request_instance.requested_coils else []

    # Cambiar el estado de las bobinas a estatus 1
    coil.objects.filter(id__in=requested_coils_ids).update(FK_coilStatus_id=coilStatus.objects.get(id=1))

    # Eliminar la solicitud
    coil_request_instance.delete()

    return redirect(reverse('coil-request'))
