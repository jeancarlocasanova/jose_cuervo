from django.shortcuts import render

def reports_view(request):
    return render(request, "cuervo/report.html")