from django.shortcuts import render, redirect, get_object_or_404
from ..models import label, coil, labelStatus, init_label
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from ..form import FilterLabelForm, UpdateLabelForm, LabelInitForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
import csv
from datetime import datetime

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

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_canceled(request):
        msg = None
        issaved = None
        if request.method == "POST":
            form = LabelInitForm(request.POST)
            if form.is_valid():
                csv_files = request.FILES.getlist('csv_file')
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

        return render(request, "cuervo/label_canceled.html", {"form": form, "msg": msg})

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def init_label_in_inventory(request):
        msg = None
        issaved = None
        if request.method == "POST":
            form = LabelInitForm(request.POST)
            if form.is_valid():
                csv_files = request.FILES.getlist('csv_file')
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

        return render(request, "cuervo/label_in_inventory.html", {"form": form, "msg": msg})