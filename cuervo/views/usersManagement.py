from django.shortcuts import render

def usersManagement_view(request):
    return render(request, "cuervo/usersManagement.html")