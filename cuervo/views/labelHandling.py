from django.shortcuts import render

def labelHandling_view(request):
    return render(request, "cuervo/labelHandling.html")