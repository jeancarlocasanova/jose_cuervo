from django.shortcuts import render, redirect
from ..models import coilStatus
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from ..form import CoilStatusForm, EditCoilStatusForm

def coilHandling_view(request):
    return render(request, "cuervo/coilHandling.html")

def coilStatus_view(request):
    coil_status = coilStatus.objects.all()
    return render(request, "cuervo/coilStatus.html", {'coil_status': coil_status})

class deleteCoilStatus_view(DeleteView):
    model = coilStatus
    template_name = 'cuervo/coil_status_confirm_delete.html'
    success_url = reverse_lazy('coilStatus')

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

def updateCoilStatus_view(request, id):
    form = EditCoilStatusForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                status = coilStatus.objects.get(id=id)
                if status is not None:
                    status.name = name
                    status.description = description
                    status.save()
                    return redirect("/coilStatus/")
            except coilStatus is None:
                msg = 'Error'
        else:
            msg = 'Error validando el formulario'

    return render(request, "cuervo/coil_status_edit.html", {"form": form, "msg": msg})