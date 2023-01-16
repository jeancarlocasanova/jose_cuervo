from django.shortcuts import render

def inventoryLocation_view(request):
    return render(request, "cuervo/inventoryLocation.html")