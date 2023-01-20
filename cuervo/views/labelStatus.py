from django.shortcuts import render, redirect
from ..models import labelStatus
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from ..form import LabelStatusForm, EditLabelStatusForm

def labelStatus_view(request):
    label_status = labelStatus.objects.all()
    return render(request, "cuervo/labelStatus.html", {'label_status': label_status})

class deleteStatus_view(DeleteView):
    model = labelStatus
    template_name = 'cuervo/status_confirm_delete.html'
    success_url = reverse_lazy('labelStatus')

def createStatus_view(request):
    msg = None
    if request.method == "POST":
        form = LabelStatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                inventoryObj = labelStatus.objects.get(name=name)
            except:
                inventoryObj = None

            if inventoryObj is None:
                inventoryObj = labelStatus.objects.create(name=name, description=description)
                inventoryObj.save()
                return redirect("/labelStatus/")
            else:
                msg = 'Este Nombre de usuario ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = LabelStatusForm()

    return render(request, "cuervo/status_create.html", {"form": form, "msg": msg})

def updateStatus_view(request, id):
    form = EditLabelStatusForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                status = labelStatus.objects.get(id=id)
                if status is not None:
                    status.name = name
                    status.description = description
                    status.save()
                    return redirect("/labelStatus/")
            except labelStatus is None:
                msg = 'Error'
        else:
            msg = 'Error validando el formulario'

    return render(request, "cuervo/status_edit.html", {"form": form, "msg": msg})