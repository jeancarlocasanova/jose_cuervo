from django.shortcuts import render, redirect
from ..models import coilStatus, coilType, coilProvider, coil, label
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import CoilStatusForm, CoilProviderForm, CoilTypeForm, CreateCoilForm, UpdateCoilForm, FilterCoilForm,DeleteLabelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError
from django.forms import formset_factory
import csv

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
def coil_view(request):
    coilList = coil.objects.all()
    if request.method == 'POST':
        form = FilterCoilForm(request.POST)
        if form.is_valid():
            boxNumber = form.cleaned_data['boxNumber']
            purchaseOrder = form.cleaned_data['purchaseOrder']
            if boxNumber and boxNumber >= 0:
                coilList = coilList.filter(boxNumber=boxNumber)
            if purchaseOrder:
                coilList = coilList.filter(purchaseOrder=purchaseOrder)
            return render(request, "cuervo/coil.html", {'coilList': coilList})
    else:
        form = FilterCoilForm()
    return render(request, 'cuervo/coilFilterForm.html', {'form': form})


class updateCoil_view(PermissionRequiredMixin, UpdateView):
    model = coil
    template_name = 'cuervo/coil_edit.html'
    success_url = reverse_lazy('coil')
    form_class = UpdateCoilForm
    permission_required = 'cuervo.change_coil'

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(last_edit_user=owner)

@permission_required('cuervo.add_coil', login_url='/login/')
def createCoil_view(request):
    msg = None
    labels = []

    if request.method == "POST":
        form = CreateCoilForm(request.POST)
        if form.is_valid():
            csv_files = request.FILES.getlist('csv_file')

            numrollo = form.cleaned_data.get("numrollo")
            boxNumber = form.cleaned_data.get("boxNumber")
            notDelivered = form.cleaned_data.get("notDelivered")
            purchaseOrder = form.cleaned_data.get("purchaseOrder")
            FK_labelStatus_id = form.cleaned_data.get("FK_labelStatus_id")
            FK_inventoryLocation_id = form.cleaned_data.get("FK_inventoryLocation_id")
            FK_sku_id = form.cleaned_data.get("FK_sku_id")
            FK_coilStatus_id = form.cleaned_data.get("FK_coilStatus_id")
            FK_coilType_id = form.cleaned_data.get("FK_coilType_id")
            FK_coilProvider_id = form.cleaned_data.get("FK_coilProvider_id")
            last_edit_user = request.user

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
                if (textos != [] and len(textos) > notDelivered + 1) and (
                        folios_filtrado != [] and len(folios_filtrado) > notDelivered + 1) and not duplicates:

                    try:
                        coilObj = coil.objects.filter(numrollo__in=numrollo, FK_coilType_id__in=FK_coilType_id)
                    except:
                        coilObj = None
                    if coilObj is None:
                        delivered = len(textos)
                        missing = delivered - notDelivered
                        coilObj = coil.objects.create(notDelivered=notDelivered,
                                                      numrollo=numrollo, purchaseOrder=purchaseOrder,
                                                      boxNumber=boxNumber, missing=missing,
                                                      FK_sku_id=FK_sku_id, FK_coilStatus_id=FK_coilStatus_id,
                                                      FK_coilType_id=FK_coilType_id,
                                                      FK_coilProvider_id=FK_coilProvider_id,
                                                      last_edit_user=last_edit_user, delivered=delivered)

                        data_exists = label.objects.filter(uniqueid__in=textos, url__in=folios_filtrado)
                        folios_filtrado = [valor for valor in folios_filtrado if valor.strip()]
                        if not data_exists:
                            try:
                                if len(folios_filtrado) == len(textos):
                                    for index, x in enumerate(folios_filtrado):
                                        labelObj = label.objects.create(
                                            uniqueid=folios_filtrado[index],
                                            url=textos[index],
                                            FK_coil_id=coilObj,
                                            FK_labelStatus_id=FK_labelStatus_id,
                                            FK_inventoryLocation_id=FK_inventoryLocation_id,
                                            last_edit_user=last_edit_user
                                        )
                                        labelObj.save()
                                    coilObj.save()
                            except Exception as e:
                                label.objects.filter(FK_coil_id=coilObj).delete()
                                coil.objects.filter(id=coilObj.id).delete()
                                msg = "Error al generar marbetes" + str(e)
                        else:
                            msg = "Algunos de estos marbetes ya existen"
                    else:
                        msg = 'Error al generar la bobina'
                else:
                    if duplicates:
                        # Aquí puedes trabajar con los datos repetidos
                        for index in duplicates:
                            print(f"El texto '{textos[index]}' está repetido en el folio: {folios[index]}.")
                    else:
                        msg = 'Revisa si los números de folio o los folios no entregados estén bien'
        else:
            msg = 'Ha ocurrido un error'
            print(form.errors)
    else:
        form = CreateCoilForm()

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

