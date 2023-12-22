from django.shortcuts import render, redirect
from ..models import order, order_Exec, coil, order_Label, label
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import OrderForm, AssignOrderForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError

# <------ ORDER CRUD --------!>

def Order_view(request):
    ObjOrder = order.objects.all()
    return render(request, "cuervo/Order.html", {'order': ObjOrder})

class deleteOrder_view(PermissionRequiredMixin, DeleteView):
    model = order
    template_name = 'cuervo/order_confirm_delete.html'
    success_url = reverse_lazy('Order')
    permission_required = 'cuervo.delete_order'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tittle = "A ocurrido un error"
        msg = "No se puede eliminar este dato debido a que esta asignado a un registro"
        isError = False
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            isError = True
        finally:
            if(isError):
                return render(request, "cuervo/display_error.html", {"tittle": tittle, "msg": msg, "link": success_url})
            else:
                return redirect(success_url)


class updateOrder_view(PermissionRequiredMixin, UpdateView):
    model = order
    template_name = 'cuervo/order_edit.html'
    success_url = reverse_lazy('Order')
    form_class = OrderForm
    permission_required = 'cuervo.change_order'

@permission_required('cuervo.add_order', login_url='/login/')
def createOrder_view(request):
    msg = None
    objCoils = None
    ids_str = ""  # Initialize ids_str
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data.get("uniqueid")
            FK_sku_id = form.cleaned_data.get("FK_sku_id")
            status = form.cleaned_data.get("status")
            lote = form.cleaned_data.get("lot")
            try:
                OrderObj = order.objects.get(uniqueid=uniqueid)
            except order.DoesNotExist:
                OrderObj = None

            if OrderObj is None:
                try:
                    # Get all coils related to the order
                    objCoils = coil.objects.filter(orderUniqueid=uniqueid)
                    for a in objCoils:
                        ids_str += str(a.id) + ", "
                    # Remove the trailing comma and space
                    ids_str = ids_str[:-2]

                    # Retrieve labels for coils with status 'Disponible'
                    available_labels = label.objects.filter(
                        FK_coil_id__in=objCoils,
                        FK_labelStatus_id__name='Disponible'
                    )

                    # Create order and associate coils
                    OrderObj = order.objects.create(
                        uniqueid=uniqueid,
                        FK_sku_id=FK_sku_id,
                        status=status,
                        lot=lote,
                        coils=ids_str
                    )
                    OrderObj.save()

                    # Create order_Label instances for each label and order pair
                    for label_obj in available_labels:
                        order_label = order_Label.objects.create(
                            FK_label_id=label_obj,
                            FK_order_id=OrderObj
                        )
                        order_label.save()

                    return redirect("/Order/")
                except Exception as e:
                    print(str(e))
                    msg = 'Ha ocurrido un error al crear la orden'
            else:
                msg = 'Esta Orden ya existe'
        else:
            msg = 'Ha ocurrido un error'
    else:
        form = OrderForm()

    return render(request, "cuervo/order_create.html", {"form": form, "msg": msg})



# <------ ASSIGN ORDER --------!>
def assign_view(request):
    requestObj = order_Exec.objects.all()
    return render(request, "cuervo/view_order_assign.html", {'order': requestObj})

@permission_required('cuervo.add_order_exec', login_url='/login/')
def assignOrder_view(request):
    msg = None
    if request.method == "POST":
        form = AssignOrderForm(request.POST)
        if form.is_valid():
            FK_order_id = form.cleaned_data.get("FK_order_id")
            FK_line_id = form.cleaned_data.get("FK_line_id")
            try:
                requestObj = order_Exec.objects.create(FK_order_id=FK_order_id, FK_line_id=FK_line_id)
                requestObj.save()
            except:
                requestObj = None
            if requestObj is None:
                msg = 'No se le puede Asignar varias ordenes a una Linea'
            else:
                return redirect("/assign/")
        else:
            msg = 'A ocurrido un error'
    else:
        form = AssignOrderForm()

    return render(request, "cuervo/assign_order.html", {"form": form, "msg": msg})

class StopOrder_view(PermissionRequiredMixin, DeleteView):
    model = order_Exec
    template_name = 'cuervo/order_Exec_confirm_delete.html'
    success_url = reverse_lazy('assign')
    permission_required = 'cuervo.delete_order_exec'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        tittle = "A ocurrido un error"
        msg = "No se puede eliminar este dato debido a que esta asignado a un registro"
        isError = False
        try:
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            isError = True
        finally:
            if(isError):
                return render(request, "cuervo/display_error.html", {"tittle": tittle, "msg": msg, "link": success_url})
            else:
                return redirect(success_url)