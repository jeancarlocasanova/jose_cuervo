from django.shortcuts import render

def labelStatus_view(request):
    return render(request, "cuervo/labelStatus.html")