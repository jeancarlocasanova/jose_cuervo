from django.shortcuts import render, redirect, get_object_or_404
from ..models import label, coil, labelStatus, init_label, coilStatus,coilType, inventoryLocation
from django.views.generic import UpdateView, CreateView
from django.urls import reverse_lazy
from ..form import FilterLabelForm, UpdateLabelForm, LabelInitForm, ZipForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import csv
from datetime import datetime
from django.contrib import messages
from openpyxl import load_workbook
import re

def labelHandling_view(request):
    labelList = label.objects.all()
    if request.method == 'POST':
        form = FilterLabelForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data['uniqueid']
            if uniqueid and len(uniqueid) >= 0:
                labelList = labelList.filter(uniqueid__contains=uniqueid)
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
    return render(request, "cuervo/coil_createv2.html")

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
