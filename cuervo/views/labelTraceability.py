from django.shortcuts import render

def labelTraceability_view(request):
    return render(request, "cuervo/labelTraceability.html")