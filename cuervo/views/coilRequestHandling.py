from django.shortcuts import render, redirect
from ..models import order, lot, coil, coil_request, coil_request_status, coilStatus, granel_lot
from django.views.generic import DeleteView, UpdateView, CreateView
from django.urls import reverse_lazy
from ..form import CoilRequestForm, CoilRequestFilter, CreateCoilFormv2
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

@permission_required('cuervo.view_coil_request', login_url='/login/')
def coilRequest_view(request):
    requestCoil = coil_request.objects.all()
    statusRequest = coil_request_status.objects.all()
    if request.method == 'POST':
        form = CoilRequestFilter(request.POST)
        if form.is_valid():
            statusID = form.cleaned_data['Fk_coil_request_status']
            if statusID:
                statusID = statusID.id
                requestCoil = requestCoil.filter(FK_coil_request_status_id=statusID)
                statusRequest = statusRequest.filter(id=statusID).first()
                print(statusRequest)
                statusreq = statusRequest.status
                print(statusreq)
            return render(request, "cuervo/coilRequest.html", {'coil_request': requestCoil, 'statusRequest': statusreq})
    else:
        form = CoilRequestFilter()
    return render(request, 'cuervo/coilRequestFilterForm.html', {'form': form})

class updateCoilRequest_view(PermissionRequiredMixin, UpdateView):
    model = coil_request
    template_name = 'cuervo/coil_request_update.html'
    success_url = reverse_lazy('coil-request')
    form_class = CoilRequestForm
    permission_required = 'cuervo.change_coil_request'

class deleteCoilRequest_view(PermissionRequiredMixin, DeleteView):
    model = coil_request
    template_name = 'cuervo/coil_request_confirm_delete.html'
    success_url = reverse_lazy('coil-request')
    permission_required = 'cuervo.delete_coil_request'

def createCoilRequest(request):
    msg = None
    orden = None
    bobinas = []
    selected_order_coils = []
    marbetes_necesarios = 0
    marbetes_totales = 0


    if request.method == "POST":
        form = CreateCoilFormv2(request.POST)

        if 'buscar' in request.POST and form.is_valid():
            ordenproduccion = form.cleaned_data.get("ordenproduccion")
            try:
                orden = order.objects.get(uniqueid=ordenproduccion)
                if orden.status == 'REL' or orden.status == 'CRTD':

                    selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []
                    bobinas = coil.objects.filter(id__in=selected_order_coils,
                                                FK_coilStatus_id=coilStatus.objects.get(name='Asignada'))

                
                elif orden.status == 'TECO':
                    msg = 'Orden de producción cerrada'
            except order.DoesNotExist:
                msg = 'Orden de producción no encontrada'

        elif 'seleccionar' in request.POST:
            marbetes_necesarios = int(request.POST.get('marbetes_necesarios', 0))
            ordenproduccion = request.POST.get("ordenproduccion")
            try:
                orden = order.objects.get(uniqueid=ordenproduccion)
                selected_order_coils = [int(id) for id in orden.coils.split(',')] if orden.coils else []
                bobinas = coil.objects.filter(FK_coilStatus_id=coilStatus.objects.get(name='Asignada'))

                total_marbetes = 0
                selected_bobinas_ids = []
                for bobina in bobinas:
                    if total_marbetes < marbetes_necesarios:
                        total_marbetes += bobina.missing
                        selected_bobinas_ids.append(bobina.id)

                for bobina in bobinas:
                    bobina.selected = bobina.id in selected_bobinas_ids

                marbetes_totales = total_marbetes

            except order.DoesNotExist:
                msg = 'Orden de producción no encontrada'

        elif 'crear' in request.POST and form.is_valid():
            bobinas_seleccionadas_str = request.POST.get('current_bobinas', '')
            bobinas_seleccionadas = [int(id) for id in bobinas_seleccionadas_str.split(',') if id.isdigit()]

            ordenproduccion = form.cleaned_data.get("ordenproduccion")

            if not bobinas_seleccionadas:
                msg = 'Debe seleccionar al menos una bobina para generar la solicitud.'
            else:
                orden = order.objects.get(uniqueid=ordenproduccion)
                if not orden:
                    msg = 'Orden de producción no seleccionada.'
                else:
                    total_quantity = int(request.POST.get('total_quantity_hidden', 0))

                    # Verificar si ya existe una solicitud similar
                    solicitud_existente = coil_request.objects.filter(
                        FK_order_id=orden,
                        requested_coils=bobinas_seleccionadas_str,
                        FK_coil_request_status_id=coil_request_status.objects.get(status='Pendiente')
                    ).exists()

                    if not solicitud_existente:
                        nueva_solicitud = coil_request.objects.create(
                            FK_order_id=orden,
                            requested_coils=bobinas_seleccionadas_str,
                            request_date=timezone.now(),
                            FK_coil_request_status_id=coil_request_status.objects.get(status='Pendiente'),
                            created_by=request.user,
                            total_number=total_quantity
                        )

                        coil_status_solicitada = coilStatus.objects.get(id=4)
                        coil.objects.filter(id__in=bobinas_seleccionadas).update(FK_coilStatus_id=coil_status_solicitada)

                        return HttpResponse("""
                                                <script>
                                                    alert('La solicitud se ha actualizado correctamente.');
                                                    window.location.href = '/coil-request/';
                                                </script>
                                            """)

    else:
        form = CreateCoilFormv2()

    return render(request, "cuervo/coil_request_create.html", {
        "form": form,
        "msg": msg,
        "bobinas": bobinas,
        "orden": orden,
        "selected_order_coils": selected_order_coils,
        "marbetes_necesarios": marbetes_necesarios,
        "marbetes_totales": marbetes_totales
    })


#----------------- Coil Request Status -----------------

def coilRequestStatus_view(request):
    requestCoilStatus = coil_request_status.objects.all()
    return render(request, "cuervo/coilRequestStatus.html", {'status': requestCoilStatus})


class createCoilRequestStatus_view(PermissionRequiredMixin, CreateView):
    model = coil_request_status
    template_name = 'cuervo/coil_status_request_create.html'
    success_url = reverse_lazy('coil-request-status')
    fields = ['status']
    permission_required = 'cuervo.add_coil_request_status'

class updateCoilRequestStatus_view(PermissionRequiredMixin, UpdateView):
    model = coil_request_status
    template_name = 'cuervo/coil_request_status_update.html'
    success_url = reverse_lazy('coil-request-status')
    fields = ['status']
    permission_required = 'cuervo.change_coil_request_status'

class deleteCoilRequestStatus_view(PermissionRequiredMixin, DeleteView):
    model = coil_request_status
    template_name = 'cuervo/coil_request_status_confirm_delete.html'
    success_url = reverse_lazy('coil-request-status')
    permission_required = 'cuervo.delete_coil_request_status'

# ----------------- Coil acept request -----------------
@permission_required('auth.authorize_label', login_url='/login/')
def CoilRequestHandling_view(request):
    statusList = coil_request.objects.all()
    statusList = statusList.filter(FK_coil_request_status_id__id=4)
    return render(request, "cuervo/coilRequestHandling.html", {'statusList': statusList})

@permission_required('auth.authorize_label', login_url='/login/')
@require_http_methods(['POST'])
def AcceptCoilRequest(request, pk):
    status = coil_request_status.objects.filter(status='Aceptada').first()
    ObjCoilRequest= coil_request.objects.filter(id=pk).first()
    ObjCoilRequest.FK_coil_request_status_id = status
    ObjCoilRequest.accepted_by = request.user
    ObjCoilRequest.save()
    return redirect('coilRequestHandling')

@require_http_methods(['POST'])
def DeclineCoilRequest(request, pk):
    status = coil_request_status.objects.filter(status='Declinada').first()
    ObjCoilRequest = coil_request.objects.filter(id=pk).first()
    ObjCoilRequest.FK_coil_request_status_id = status
    ObjCoilRequest.accepted_by = request.user
    ObjCoilRequest.save()
    return redirect('coilRequestHandling')

