from django.shortcuts import render, redirect
from ..models import order
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import OrderForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# <------ ORDER CRUD --------!>

def Order_view(request):
    ObjOrder = order.objects.all()
    return render(request, "cuervo/Order.html", {'order': ObjOrder})

class deleteOrder_view(PermissionRequiredMixin, DeleteView):
    model = order
    template_name = 'cuervo/order_confirm_delete.html'
    success_url = reverse_lazy('Order')
    permission_required = 'cuervo.delete_order'


class updateOrder_view(PermissionRequiredMixin, UpdateView):
    model = order
    template_name = 'cuervo/order_edit.html'
    success_url = reverse_lazy('Order')
    form_class = OrderForm
    permission_required = 'cuervo.change_order'

@permission_required('cuervo.add_order', login_url='/login/')
def createOrder_view(request):
    msg = None
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data.get("uniqueid")
            FK_sku_id = form.cleaned_data.get("FK_sku_id")
            try:
                OrderObj = order.objects.get(uniqueid=uniqueid)
            except:
                OrderObj = None
            if OrderObj is None:
                OrderObj = order.objects.create(uniqueid=uniqueid, FK_sku_id=FK_sku_id)
                OrderObj.save()
                return redirect("/Order/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = OrderForm()

    return render(request, "cuervo/order_create.html", {"form": form, "msg": msg})