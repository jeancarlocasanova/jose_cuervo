from django.shortcuts import render

def configurationMenu_view(request):
    return render(request,"cuervo/configuration_menu.html")

def orderMenu_view(requets):
    return render(requets, "cuervo/order_menu.html")

def labelMenu_view(request):
    return render(request, "cuervo/label_menu.html")

def reports_view(request):
    return render(request, "cuervo/report.html")
