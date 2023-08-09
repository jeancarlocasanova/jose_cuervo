from django.shortcuts import render, redirect, get_object_or_404
from ..models import label, coil, labelStatus
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

#<----------------------- Search Label By Coil ID -------------------------------->
def searchLabelByCoilFK(request, pk):
    coilFk = get_object_or_404(coil, id=pk)
    labels = label.objects.filter(FK_coil_id=coilFk)
    coil_not_delivered = coilFk.notDelivered

    if request.method == 'POST':
        selected_labels = request.POST.getlist('selected_labels')
        faltante = request.POST.get('faltante', 'off')

        selected_labels_count = len(selected_labels)
        faltante_labels_count = labels.filter(FK_labelStatus_id__name='Faltante').count()

        if faltante == 'on':
            faltante_labels_count += selected_labels_count

        if faltante_labels_count <= coil_not_delivered:
            for label_id in selected_labels:
                label_obj = label.objects.get(id=label_id)
                if faltante == 'on':
                    label_obj.FK_labelStatus_id = labelStatus.objects.get(name='Faltante')
                else:
                    label_obj.FK_labelStatus_id = labelStatus.objects.get(name='Faltante')  # Define your other status
                label_obj.save()

        # Redirect to the same page to avoid form resubmission
        return redirect('label-find', pk=pk)

    total_labels = labels.count()
    faltante_labels = labels.filter(FK_labelStatus_id__name='Faltante').count()

    disable_checkboxes = faltante_labels >= coil_not_delivered

    return render(request, 'cuervo/label_by_CoilFk.html', {
        'labels': labels,
        'disable_checkboxes': disable_checkboxes,
    })
