from django.shortcuts import render, redirect
from ..models import inventoryLocation
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from ..form import EditInventoryLocationForm, InventoryLocationForm

def inventoryLocation_view(request):
    inventory = inventoryLocation.objects.all()
    return render(request, "cuervo/inventoryLocation.html", {'inventory': inventory})
class deleteLocation_view(DeleteView):
    model = inventoryLocation
    template_name = 'cuervo/location_confirm_delete.html'
    success_url = reverse_lazy('inventoryLocation')

def createLocation_view(request):
    msg = None
    if request.method == "POST":
        form = InventoryLocationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                inventoryObj = inventoryLocation.objects.get(name=name)
            except:
                inventoryObj = None

            if inventoryObj is None:
                inventoryObj = inventoryLocation.objects.create(name=name, description=description)
                inventoryObj.save()
                return redirect("/inventoryLocation/")
            else:
                msg = 'Este Nombre de usuario ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = InventoryLocationForm()

    return render(request, "cuervo/location_create.html", {"form": form, "msg": msg})

def updateLocation_view(request, id):
    form = EditInventoryLocationForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                inventory = inventoryLocation.objects.get(id=id)
                #form = EditInventoryLocationForm(instance=inventory)
                if inventory is not None:
                    inventory.name = name
                    inventory.description = description
                    inventory.save()
                    return redirect("/inventoryLocation/")
            except inventoryLocation is None:
                msg = 'Error'
        else:
            msg = 'Error validando el formulario'

    return render(request, "cuervo/location_edit.html", {"form": form, "msg": msg})