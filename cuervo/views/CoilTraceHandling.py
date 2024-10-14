from django.shortcuts import render, redirect, get_object_or_404
from ..models import coilTrace, order, coil, lot, coilStatus,label, labelStatus, granel_lot
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import CoilTraceForm, UpdateCoilTraceForm, orderForm2, LotSelectionForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.db.models import Q

@permission_required('auth.return_coils', login_url='/login/')
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
                    if devolution:
                        id_order = devolution.id
                        return redirect(f"/coilreturn/{id_order}")
                    else:
                        messages.error(request, 'Orden no encontrada')
                except order.DoesNotExist:
                    messages.error(request, 'No se ha encontrado ninguna orden de producción con el ID proporcionado.')
            else:
                messages.error(request, 'El formulario no es válido. Por favor, revise los datos ingresados.')
    else:
        form = orderForm2()

    return render(request, 'cuervo/return_of_coils_filter.html', {'form': form, "msg": msg})

@permission_required('auth.return_coils', login_url='/login/')
def returnOfCoils(request, order_id):
    order_obj = get_object_or_404(order, id=order_id)
    consume_status = get_object_or_404(coilStatus, name='Consumida')

    coilsWithComa = order_obj.coils
    coilsWithComaList = coilsWithComa.split(',') if coilsWithComa else []
    coil_list = coil.objects.filter(id__in=coilsWithComaList)
    coil_list = coil_list.exclude(FK_coilStatus_id=consume_status)

    # Validar etiquetas disponibles o asignadas
    assigned_status = get_object_or_404(labelStatus, name='Asignado')
    available_status = get_object_or_404(labelStatus, name='Disponible')

    valid_coils = []
    for coil_item in coil_list:
        if label.objects.filter(FK_coil_id=coil_item).filter(
                Q(FK_labelStatus_id=assigned_status) | Q(FK_labelStatus_id=available_status)).exists():
            valid_coils.append(coil_item)
    print(valid_coils)
    coil_list = valid_coils

    if request.method == "POST":
        selected_coils_ids = [key.split('selected_coils')[1] for key in request.POST.keys() if 'selected_coils' in key]
        selected_coils = coil.objects.filter(id__in=selected_coils_ids)

        if not selected_coils.exists():
            messages.error(request, 'No se seleccionaron bobinas para devolver.')
            return redirect(request.path_info)

        try:
            devolved_status = get_object_or_404(coilStatus, name='Devuelta')

            for selected_coil in selected_coils:
            
                obj_coil = coil.objects.create(
                    initNumber=selected_coil.initNumber,
                    finishNumber=selected_coil.finishNumber,
                    numrollo=selected_coil.numrollo,
                    notDelivered=selected_coil.notDelivered,
                    missing=selected_coil.missing,
                    delivered=selected_coil.delivered,
                    boxNumber=selected_coil.boxNumber,
                    purchaseOrder=selected_coil.purchaseOrder,
                    orderUniqueid=selected_coil.orderUniqueid,
                    sku=selected_coil.sku,
                    qty_box=selected_coil.qty_box,
                    FK_coilStatus_id=devolved_status,
                    FK_coilType_id=selected_coil.FK_coilType_id,
                    last_edit_user=selected_coil.last_edit_user,
                    FK_coilProvider_id=selected_coil.FK_coilProvider_id
                )

                # Verifica y actualiza el folio inicial si es necesario
                labels = label.objects.filter(FK_coil_id=selected_coil).order_by('uniqueid')
                folio_final_num = int(selected_coil.finishNumber.split('-')[-1])
                folio_inicial_num = int(selected_coil.initNumber.split('-')[-1])

                labels_with_different_status = labels.exclude(
                    Q(FK_labelStatus_id=assigned_status) | Q(FK_labelStatus_id=available_status))

                # Lógica para encontrar un grupo de folios consecutivos al principio
                consecutive_count = 0
                new_folio_inicial = None
                prev_label_number = None

                for lbl in labels_with_different_status:
                    label_number = int(lbl.uniqueid.split('-')[-1])

                    if prev_label_number is None:
                        prev_label_number = label_number
                        consecutive_count = 1
                    elif label_number == prev_label_number + 1:
                        consecutive_count += 1
                        prev_label_number = label_number
                    else:
                        break

                    if consecutive_count >= 5:  # Comprueba si hay al menos 5 consecutivos al principio
                        new_folio_inicial = label_number

                if new_folio_inicial is not None:
                    # Actualizar el initNumber del obj_coil con el nuevo folio inicial
                    obj_coil.initNumber = f'Ne-{new_folio_inicial + 1:010}'
                    obj_coil.save()

                    # Actualizar el finishNumber del selected_coil con new_folio_inicial - 1
                    selected_coil.finishNumber = f'Ne-{new_folio_inicial - 1:010}'
                    selected_coil.save()

                    # Calcular missing para selected_coil y obj_coil
                    missing_count = folio_final_num - new_folio_inicial
                    missing_count = missing_count - selected_coil.notDelivered

                    obj_coil.missing = missing_count - 1
                    obj_coil.save()
                    
                    missing_count = (new_folio_inicial - 1)  - folio_inicial_num
                    missing_count = missing_count - selected_coil.notDelivered

                    selected_coil.missing = missing_count
                    selected_coil.save()

                if new_folio_inicial is not None:
                    coilTrace.objects.create(
                        FK_coil_id=selected_coil,
                        user_id=request.user,
                        FK_order_id=order_obj,
                        initLabel=selected_coil.initNumber,
                        lastLabel=selected_coil.finishNumber,
                        total_label=selected_coil.missing + 1
                    )
                else:
                    coilTrace.objects.create(
                        FK_coil_id=selected_coil,
                        user_id=request.user,
                        FK_order_id=order_obj,
                        initLabel=selected_coil.initNumber,
                        lastLabel=selected_coil.finishNumber,
                        total_label=selected_coil.missing
                    )

            messages.success(request, 'Las bobinas seleccionadas han sido devueltas exitosamente.')
        except Exception as e:
            messages.error(request, f'Hubo un error al devolver las bobinas: {str(e)}')

        return redirect(request.path_info)

    return render(request, "cuervo/return_of_coils.html", {"coils": coil_list, "order": order_obj})

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

