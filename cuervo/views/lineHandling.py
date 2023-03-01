from django.shortcuts import render, redirect
from ..models import line
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import LineForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import ProtectedError

# <------ LINE CRUD --------!>

def Line_view(request):
    ObjLine = line.objects.all()
    return render(request, "cuervo/Line.html", {'line': ObjLine})

class deleteLine_view(PermissionRequiredMixin, DeleteView):
    model = line
    template_name = 'cuervo/line_confirm_delete.html'
    success_url = reverse_lazy('Line')
    permission_required = 'cuervo.delete_line'

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


class updateLine_view(PermissionRequiredMixin, UpdateView):
    model = line
    template_name = 'cuervo/line_edit.html'
    success_url = reverse_lazy('Line')
    fields = ['uniqueid']
    permission_required = 'cuervo.change_line'

@permission_required('cuervo.add_line', login_url='/login/')
def createLine_view(request):
    msg = None
    if request.method == "POST":
        form = LineForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data.get("uniqueid")
            try:
                LineObj = line.objects.get(uniqueid=uniqueid)
            except:
                LineObj = None
            if LineObj is None:
                LineObj = line.objects.create(uniqueid=uniqueid)
                LineObj.save()
                return redirect("/Line/")
            else:
                msg = 'Este Nombre ya existe'
        else:
            msg = 'A ocurrido un error'
    else:
        form = LineForm()

    return render(request, "cuervo/line_create.html", {"form": form, "msg": msg})