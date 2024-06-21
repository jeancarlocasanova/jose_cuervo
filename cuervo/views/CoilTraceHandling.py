from django.shortcuts import render, redirect, get_object_or_404
from ..models import coilTrace, order, coil, lot, coilStatus,label, labelStatus, granel_lot
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import CoilTraceForm, UpdateCoilTraceForm, orderForm2, LotSelectionForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q

def returnOfCoilsFilter(request):
    form = orderForm2()
    lot_form = None
    coil_form = None
    msg = None
    if request.method == "POST":
        if 'order_form' in request.POST:
            form = orderForm2(request.POST)
            if form.is_valid():
                uniqueid = form.cleaned_data.get("uniqueid")
                try:
                    devolution = order.objects.get(uniqueid=uniqueid)
                    orderLots = lot.objects.filter(FK_order_id=devolution)
                    lot_form = LotSelectionForm(queryset=orderLots)
                    return render(request, "cuervo/return_of_coils_lot.html", {
                        "form": form,
                        "lot_form": lot_form,
                        "devolution": devolution,
                        "orderLots": orderLots
                    })
                except order.DoesNotExist:
                    msg = 'No se ha encontrado ninguna orden de producción con el ID proporcionado.'
            else:
                msg = 'El formulario no es válido. Por favor, revise los datos ingresados.'
        elif 'lot_form' in request.POST:
            lot_value = request.POST.get("lote")
            lot_obj = lot.objects.get(id=lot_value)
            id_order =lot_obj.FK_order_id.id
            return redirect(f"/coilreturn/{lot_value}/{id_order}")
    else:
        form = orderForm2()

    return render(request, 'cuervo/return_of_coils_filter.html', {'form': form, "msg": msg})

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def returnOfCoils(request, lot_id, order_id):
    lot_obj = get_object_or_404(lot, id=lot_id)
    order_obj = get_object_or_404(order, id=order_id)
    granel_obj = granel_lot.objects.filter(FK_order_id__id=order_id)

    coilsWithComa = order_obj.coils
    coilsWithComaList = coilsWithComa.split(',') if coilsWithComa else []
    coil_list = coil.objects.filter(id__in=coilsWithComaList)

    if request.method == "POST":
        selected_coils_ids = [key.split('selected_coils')[1] for key in request.POST.keys() if 'selected_coils' in key]
        selected_coils = coil.objects.filter(id__in=selected_coils_ids)

        if not selected_coils.exists():
            messages.error(request, 'No se seleccionaron bobinas para devolver.')
            return redirect(request.path_info)

        try:
            devolved_status = get_object_or_404(coilStatus, name='Devuelta')
            assigned_status = get_object_or_404(labelStatus, name='Asignado')
            available_status = get_object_or_404(labelStatus, name='Disponible')

            for selected_coil in selected_coils:
                # Actualiza el estado de la bobina
                selected_coil.FK_coilStatus_id = devolved_status
                selected_coil.save()

                # Verifica y actualiza el folio inicial si es necesario
                labels = label.objects.filter(FK_coil_id=selected_coil).order_by('uniqueid')
                folio_final_num = int(selected_coil.finishNumber.split('-')[-1])

                labels_with_different_status = labels.exclude(Q(FK_labelStatus_id=assigned_status) | Q(FK_labelStatus_id=available_status))

                if labels_with_different_status.exists():
                    # Encuentra el primer folio que no tiene el estado diferente
                    new_folio_inicial = labels_with_different_status.last().uniqueid.split('-')[-1]
                    selected_coil.initNumber = f'{int(new_folio_inicial) + 1:010}'
                    selected_coil.save()

                    missing_count = folio_final_num - int(new_folio_inicial)
                    selected_coil.missing = missing_count
                    selected_coil.save()

            updated_coils = [str(coil_id) for coil_id in coilsWithComaList if str(coil_id) not in selected_coils_ids]
            order_obj.coils = ','.join(updated_coils)
            order_obj.save()

            messages.success(request, 'Las bobinas seleccionadas han sido devueltas exitosamente.')
        except Exception as e:
            messages.error(request, f'Hubo un error al devolver las bobinas: {str(e)}')

        return redirect(request.path_info)

    return render(request, "cuervo/return_of_coils.html", {"lot": lot_obj, "coils": coil_list, "order": order_obj, "granel": granel_obj})


@permission_required('cuervo.add_coiltrace', login_url='/login/')
def createReturnOfCoil(request):
    msg = None
    if request.method == "POST":
        form = CoilTraceForm(request.POST)
        if form.is_valid():
            FK_coil_id = form.cleaned_data.get("FK_coil_id")
            FK_coilStatus_id = form.cleaned_data.get("FK_coilStatus_id")
            FK_coilType_id = form.cleaned_data.get("FK_coilType_id")
            FK_coilProvider_id = form.cleaned_data.get("FK_coilProvider_id")
            user_id = request.user
            FK_order_id = form.cleaned_data.get("FK_order_id")
            FK_inventory_id = form.cleaned_data.get("FK_inventory_id")
            initLabel = form.cleaned_data.get("initLabel")
            IsReturned = True
            IsUsed = form.cleaned_data.get("IsUsed")
            try:
                coilTraceObj = coilTrace.objects.get(FK_coil_id=FK_coil_id,FK_order_id=FK_order_id,initLabel=initLabel, lastLabel=FK_coil_id.finishNumber)
            except:
                coilTraceObj = None

            if coilTraceObj is None:
                coilTraceObj = coilTrace.objects.create(FK_coil_id=FK_coil_id,FK_order_id=FK_order_id,initLabel=initLabel,
                                                        lastLabel=FK_coil_id.finishNumber, FK_coilStatus_id=FK_coilStatus_id,
                                                        FK_coilType_id=FK_coilType_id, FK_coilProvider_id= FK_coilProvider_id,
                                                        user_id=user_id,FK_inventory_id=FK_inventory_id,IsReturned=IsReturned,
                                                        IsUsed=IsUsed)
                coilTraceObj.save()
                return redirect("/coilreturn/")
            else:
                msg = 'Este Nombre de usuario ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = CoilTraceForm()

    return render(request, "cuervo/coil_trace_create.html", {"form": form, "msg": msg})


class deleteCoilTrace_view(PermissionRequiredMixin, DeleteView):
    model = coilTrace
    template_name = 'cuervo/coil_trace_confirm_delete.html'
    success_url = reverse_lazy('return-coil')
    permission_required = 'cuervo.delete_coiltrace'


class updateCoilTrace_view(PermissionRequiredMixin, UpdateView):
    model = coilTrace
    template_name = 'cuervo/coil_trace_edit.html'
    success_url = reverse_lazy('return-coil')
    form_class = UpdateCoilTraceForm
    permission_required = 'cuervo.change_coiltrace'

