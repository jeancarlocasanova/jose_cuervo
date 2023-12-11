from django.shortcuts import render, redirect
from ..models import coil_request, coil_request_status, label
from django.views.generic import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from ..form import CoilRequestForm, CoilProviderForm, CoilTypeForm, CreateCoilForm, UpdateCoilForm, FilterCoilForm,DeleteLabelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError, IntegerField, Value
from django.forms import formset_factory
from django.db.models import Max, CharField, Value
from django.db.models.functions import Cast
import re

def coilRequest_view(request):
    requestCoil = coil_request.objects.all()
    return render(request, "cuervo/coilRequest.html", {'coil_request': requestCoil})

class updateCoilRequest_view(PermissionRequiredMixin, UpdateView):
    model = coil_request
    template_name = 'cuervo/coil_request_update.html'
    success_url = reverse_lazy('coil-request')
    form_class = CoilRequestForm
    permission_required = 'cuervo.change_coil_request'

class deleteCoilRequest_view(PermissionRequiredMixin, DeleteView):
    model = coil_request
    template_name = 'cuervo/coil_request_confirm_delete.html'
    success_url = reverse_lazy('coil-request')
    permission_required = 'cuervo.delete_coil_request'

def createCoilRequest(request):
    msg = None
    if request.method == "POST":
        form = CoilRequestForm(request.POST)
        if form.is_valid():
            FK_coil_id = form.cleaned_data.get("FK_coil_id")
            Fk_order_id = form.cleaned_data.get("FK_order_id")
            Fk_source_invLocation_id = form.cleaned_data.get("Fk_source_invLocation_id")
            Fk_destination_invLocation_id = form.cleaned_data.get("Fk_destination_invLocation_id")
            FK_coil_request_status_id = form.cleaned_data.get("FK_coil_request_status_id")

            try:
                coilStatusObj = coil_request.objects.get(FK_coil_id=FK_coil_id, FK_order_id=Fk_order_id)
            except:
                coilStatusObj = None

            if coilStatusObj is None:
                try:
                    # Obtén el último uniqueid con labelStatus 'disponible'
                    ultimo_uniqueid_disponible = (
                        label.objects
                        .filter(FK_labelStatus_id__name__icontains='Disponible', FK_coil_id=FK_coil_id)
                        .order_by('uniqueid')
                        .values('uniqueid')
                        .first()
                    )
                    uniqueid_result = ultimo_uniqueid_disponible['uniqueid']
                    # Utilizamos expresiones regulares para extraer solo los dígitos
                    numero_result = re.sub(r'\D', '', uniqueid_result)

                    # Convertimos el resultado a un número entero
                    folio_inicial = int(numero_result)

                    folio_final = int(FK_coil_id.finishNumber)

                    coilStatusObj = coil_request.objects.create(FK_coil_id=FK_coil_id, FK_order_id=Fk_order_id,
                                                                Fk_source_invLocation_id=Fk_source_invLocation_id,
                                                                Fk_destination_invLocation_id=Fk_destination_invLocation_id,
                                                                FK_coil_request_status_id=FK_coil_request_status_id,
                                                                startingNumber=folio_inicial, endingNumber=folio_final)
                    return redirect("/coil-request/")
                except Exception as e:
                    print(str(e))
                    msg = "En esta bobina no hay ningún marbete con estado disponible"
            else:
                msg = 'Este Nombre ya existe'
        else:
            print(form.errors)
            print(form.is_bound)
            msg = 'A ocurrido un error'
    else:
        form = CoilRequestForm()

    return render(request, "cuervo/coil_request_create.html", {"form": form, "msg": msg})


#----------------- Coil Request Status -----------------

def coilRequestStatus_view(request):
    requestCoilStatus = coil_request_status.objects.all()
    return render(request, "cuervo/coilRequestStatus.html", {'status': requestCoilStatus})


class createCoilRequestStatus_view(PermissionRequiredMixin, CreateView):
    model = coil_request_status
    template_name = 'cuervo/coil_status_request_create.html'
    success_url = reverse_lazy('coil-request-status')
    fields = ['status']
    permission_required = 'cuervo.add_coil_request_status'

class updateCoilRequestStatus_view(PermissionRequiredMixin, UpdateView):
    model = coil_request_status
    template_name = 'cuervo/coil_request_status_update.html'
    success_url = reverse_lazy('coil-request-status')
    fields = ['status']
    permission_required = 'cuervo.change_coil_request_status'

class deleteCoilRequestStatus_view(PermissionRequiredMixin, DeleteView):
    model = coil_request_status
    template_name = 'cuervo/coil_request_status_confirm_delete.html'
    success_url = reverse_lazy('coil-request-status')
    permission_required = 'cuervo.delete_coil_request_status'