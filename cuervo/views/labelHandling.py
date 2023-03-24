from django.shortcuts import render, redirect
from ..models import label
from django.views.generic import DeleteView, UpdateView
from django.urls import reverse_lazy
from ..form import FilterLabelForm, UpdateLabelForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin

def labelHandling_view(request):
    labelList = label.objects.all()
    if request.method == 'POST':
        form = FilterLabelForm(request.POST)
        if form.is_valid():
            uniqueid = form.cleaned_data['uniqueid']
            FK_labelStatus_id = form.cleaned_data['FK_labelStatus_id']
            if uniqueid and len(uniqueid) >= 0:
                labelList = labelList.filter(uniqueid__contains=uniqueid)
            if FK_labelStatus_id:
                labelList = labelList.filter(FK_labelStatus_id=FK_labelStatus_id)
            return render(request, "cuervo/labelHandling.html", {'labelList': labelList})
    else:
        form = FilterLabelForm()
    return render(request, 'cuervo/labelFilterForm.html', {'form': form})

class updateLabel_view(PermissionRequiredMixin, UpdateView):
    model = label
    template_name = 'cuervo/label_edit.html'
    success_url = reverse_lazy('labelHandling')
    form_class = UpdateLabelForm
    permission_required = 'cuervo.change_label'