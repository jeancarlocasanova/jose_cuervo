from django.shortcuts import render

def depletionOfCoils_view(request):
    return render(request, "cuervo/depletionOfCoils.html")