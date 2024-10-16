from ..models import order_Exec, line, order, labelStatus, label
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.db.models import Value
from django.db.models.functions import Coalesce
from jose_cuervo.serializers import OrderSerializer
from jose_cuervo.wsgi import application

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def list_lines(request):
    lineas = line.objects.annotate(
        order=Coalesce('order_exec__FK_order_id__uniqueid', Value('Ninguna'))
    ).values('uniqueid', 'order')
    data = [{'uniqueid': linea['uniqueid'], 'order': linea['order']} for linea in lineas]
    return Response(data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def choiceField_lines(request):
    lineas = line.objects.all()
    data = [{'uniqueid': linea.uniqueid} for linea in lineas]
    return Response(data)

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def choiceField_order(request):
    # Obtener todas las órdenes cuyo estado es "abierta" y no están en el primer modelo
    orders = order.objects.filter(status='abierta').exclude(pk__in=order_Exec.objects.values_list('FK_order_id', flat=True))

    # Serializar los datos y devolverlos en formato JSON
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def create_Order(request):
    order_exec_data = request.data # obtener el objeto JSON del request
    order_id = order_exec_data.get('order')
    line_id = order_exec_data.get('line')
    print(line_id)
    lineObj = line.objects.get(uniqueid=line_id)
    orderObj = order.objects.get(uniqueid=order_id)

    # crear una instancia de order_Exec con los datos recibidos a
    try:
        order_exec = order_Exec(FK_order_id=orderObj, FK_line_id=lineObj)
        order_exec.save()
    except:
        return Response({'message': 'Error al asignar orden'})

    return Response({'message': 'Orden asignada correctamente'})

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def list_status(request):
    status = labelStatus.objects.all()
    data = [{'name': s.name, 'description': s.description} for s in status]
    return Response(data)

@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def update_label(request):
    url_label_data = request.data # obtener el objeto JSON del request
    url = url_label_data.get('url')
    statusID = url_label_data.get('status')
    try:
        labelObj = label.objects.filter(url=url).first()
        statusObj = labelStatus.objects.get(name__exact=statusID)
        # crear una instancia de order_Exec con los datos recibidos a

        labelObj.FK_labelStatus_id = statusObj
        labelObj.save()
    except Exception as e:
        return Response({'message': str(e)})

    return Response({'message': 'Status asignado correctamente'})
