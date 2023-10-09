from django.shortcuts import render
from cuervo.models import test
from django.http import HttpResponseNotFound


def test_view(request):
    try:
        latest_test = test.objects.latest('id')
    except test.DoesNotExist:
        # Si no se encuentra ningún objeto test, crea uno personalizado
        latest_test = test(url="No se encontraron registros")

    return render(request, 'cuervo/test.html', {'result': latest_test})
