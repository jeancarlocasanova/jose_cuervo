from django.shortcuts import render, redirect
from ..models import labelStatus
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import LabelStatusForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError

@permission_required('cuervo.view_labelstatus', login_url='/login/')
def labelStatus_view(request):
    label_status = labelStatus.objects.all()
    return render(request, "cuervo/labelStatus.html", {'label_status': label_status})

class deleteStatus_view(PermissionRequiredMixin, DeleteView):
    model = labelStatus
    template_name = 'cuervo/label_status_confirm_delete.html'
    success_url = reverse_lazy('labelStatus')
    permission_required = 'cuervo.delete_labelstatus'

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

class updateLabelStatus_view(PermissionRequiredMixin, UpdateView):
    model = labelStatus
    template_name = 'cuervo/label_status_edit.html'
    success_url = reverse_lazy('labelStatus')
    fields = ['name', 'description']
    permission_required = 'cuervo.change_labelstatus'

@permission_required('cuervo.add_labelstatus', login_url='/login/')
def createStatus_view(request):
    msg = None
    if request.method == "POST":
        form = LabelStatusForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            description = form.cleaned_data.get("description")
            try:
                labelStatusObj = labelStatus.objects.get(name=name)
            except:
                labelStatusObj = None

            if labelStatusObj is None:
                labelStatusObj = labelStatus.objects.create(name=name, description=description)
                labelStatusObj.save()
                return redirect("/labelStatus/")
            else:
                msg = 'Este Nombre de usuario ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = LabelStatusForm()

    return render(request, "cuervo/label_status_create.html", {"form": form, "msg": msg})
