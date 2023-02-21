from django.shortcuts import render, redirect
from ..models import coil_request_status
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import RequestStatusForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# <------ TYPE OF SKU CRUD --------!>

def requestStatus_view(request):
    request_status = coil_request_status.objects.all()
    return render(request, "cuervo/request_status.html", {'request_status': request_status})

class deleteRequestStatus_view(PermissionRequiredMixin, DeleteView):
    model = coil_request_status
    template_name = 'cuervo/request_status_confirm_delete.html'
    success_url = reverse_lazy('request-status')
    permission_required = 'cuervo.delete_coil_request_status'


class updateRequestStatus_view(PermissionRequiredMixin, UpdateView):
    model = coil_request_status
    template_name = 'cuervo/request_status_edit.html'
    success_url = reverse_lazy('request-status')
    fields = ['status']
    permission_required = 'cuervo.change_coil_request_status'

@permission_required('cuervo.add_coil_request_status', login_url='/login/')
def createRequestStatus_view(request):
    msg = None
    if request.method == "POST":
        form = RequestStatusForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.get("status")
            try:
                requestStatusObj = coil_request_status.objects.get(status=status)
            except:
                requestStatusObj = None
            if requestStatusObj is None:
                requestStatusObj = coil_request_status.objects.create(status=status)
                requestStatusObj.save()
                return redirect("/request-status/")
            else:
                msg = 'Este estatus ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = RequestStatusForm()

    return render(request, "cuervo/request_status_create.html", {"form": form, "msg": msg})