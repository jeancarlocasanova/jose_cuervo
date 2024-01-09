from django.shortcuts import render, redirect
from ..models import coilTrace, coil_request_status, label
from django.views.generic import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from ..form import CoilTraceForm, UpdateCoilTraceForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required


def returnOfCoils(request):
    coilList = coilTrace.objects.filter(IsReturned=True)
    return render(request, "cuervo/return_of_coils.html", {'coilList': coilList})


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

