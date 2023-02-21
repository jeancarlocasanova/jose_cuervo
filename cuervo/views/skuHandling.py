from django.shortcuts import render, redirect, HttpResponseRedirect
from ..models import SKU, sku_Type
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import SkuTypeForm, SkuForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError
from django.contrib import messages

# <------ TYPE OF SKU CRUD --------!>

def skuType_view(request):
    sku_type = sku_Type.objects.all()
    return render(request, "cuervo/skuType.html", {'sku_type': sku_type})

class deleteSkuType_view(PermissionRequiredMixin, DeleteView):
    model = sku_Type
    template_name = 'cuervo/sku_type_confirm_delete.html'
    success_url = reverse_lazy('skuType')
    permission_required = 'cuervo.delete_sku_type'


class updateSkuType_view(PermissionRequiredMixin, UpdateView):
    model = sku_Type
    template_name = 'cuervo/sku_type_edit.html'
    success_url = reverse_lazy('skuType')
    fields = ['name', 'description']
    permission_required = 'cuervo.change_sku_type'

@permission_required('cuervo.add_sku_type', login_url='/login/')
def createSkuType_view(request):
    msg = None
    if request.method == "POST":
        form = SkuTypeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                skuTypeObj = sku_Type.objects.get(name=name)
            except:
                skuTypeObj = None
            if skuTypeObj is None:
                skuTypeObj = sku_Type.objects.create(name=name, description=description)
                skuTypeObj.save()
                return redirect("/skuType/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = SkuTypeForm()

    return render(request, "cuervo/sku_type_create.html", {"form": form, "msg": msg})


# <------ SKU CRUD --------!>

def sku_view(request):
    sku = SKU.objects.all()
    return render(request, "cuervo/SKU.html", {'sku': sku})

class deleteSku_view(PermissionRequiredMixin, DeleteView):
    model = SKU
    template_name = 'cuervo/sku_confirm_delete.html'
    success_url = reverse_lazy('SKU')
    permission_required = 'cuervo.delete_sku'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, "custom error message")
        finally:
            return redirect(success_url)


class updateSku_view(PermissionRequiredMixin, UpdateView):
    model = SKU
    template_name = 'cuervo/sku_edit.html'
    success_url = reverse_lazy('SKU')
    form_class = SkuForm
    permission_required = 'cuervo.change_sku'

@permission_required('cuervo.add_sku', login_url='/login/')
def createSku_view(request):
    msg = None
    if request.method == "POST":
        form = SkuForm(request.POST)
        if form.is_valid():
            sku = form.cleaned_data.get("sku")
            description = form.cleaned_data.get("description")
            Fk_sku_type_id = form.cleaned_data.get("Fk_sku_type_id")
            try:
                skuObj = SKU.objects.get(sku=sku)
            except:
                skuObj = None
            if skuObj is None:
                skuObj = SKU.objects.create(sku=sku, description=description, Fk_sku_type_id=Fk_sku_type_id)
                skuObj.save()
                return redirect("/SKU/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = SkuForm()

    return render(request, "cuervo/sku_create.html", {"form": form, "msg": msg})
