from django.shortcuts import render, redirect
from ..models import coilStatus, coilType, coilProvider, coil, label, init_label, coilsInInventory, order, lot, granel_lot
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import CoilStatusForm, CoilProviderForm, CoilTypeForm, CreateCoilForm, CreateCoilFormv2, UpdateCoilForm, FilterCoilForm,DeleteLabelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError, IntegerField, Value
from django.forms import formset_factory
from django.db.models.functions import Cast
from django.db.models.expressions import RawSQL
from datetime import datetime, timedelta
from django.core.paginator import Paginator

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
        tittle = "Ha ocurrido un error"
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
    print(coilList)
    if request.method == 'POST':
        form = FilterCoilForm(request.POST)
        if form.is_valid():
            boxNumber = form.cleaned_data['boxNumber']
            purchaseOrder = form.cleaned_data['purchaseOrder']
            if boxNumber and purchaseOrder:
                coilList = coilList.filter(boxNumber=boxNumber, purchaseOrder=purchaseOrder)
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
        # Check if the user has the change_coil permission
        if self.request.user.has_perm('cuervo.change_coil'):
            # User has permission to edit any coil, so return all coils
            return self.model.objects.all()
        else:
            # User doesn't have the permission, filter by last_edit_user
            owner = self.request.user
            return self.model.objects.filter(last_edit_user=owner)

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



