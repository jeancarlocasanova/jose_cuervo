from django.shortcuts import render, redirect
from ..models import inventoryLocation
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import InventoryLocationForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

def inventoryLocation_view(request):
    inventory = inventoryLocation.objects.all()
    return render(request, "cuervo/inventoryLocation.html", {'inventory': inventory})
class deleteLocation_view(PermissionRequiredMixin, DeleteView):
    model = inventoryLocation
    template_name = 'cuervo/location_confirm_delete.html'
    success_url = reverse_lazy('inventoryLocation')
    permission_required = 'cuervo.delete_inventorylocation'

class updateLocation_view(PermissionRequiredMixin, UpdateView):
    model = inventoryLocation
    template_name = 'cuervo/location_edit.html'
    success_url = reverse_lazy('inventoryLocation')
    fields = ['name', 'description']
    permission_required = 'cuervo.change_inventorylocation'

@permission_required('cuervo.add_inventorylocation', login_url='/login/')
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