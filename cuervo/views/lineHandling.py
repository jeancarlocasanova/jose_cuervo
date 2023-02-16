from django.shortcuts import render, redirect
from ..models import line
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import LineForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

# <------ LINE CRUD --------!>

def Line_view(request):
    ObjLine = line.objects.all()
    return render(request, "cuervo/Line.html", {'line': ObjLine})

class deleteLine_view(PermissionRequiredMixin, DeleteView):
    model = line
    template_name = 'cuervo/line_confirm_delete.html'
    success_url = reverse_lazy('Line')
    permission_required = 'cuervo.delete_line'


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