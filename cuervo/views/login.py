from ..form import LoginForm
from django.contrib.auth import login, get_user_model, logout
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token

User = get_user_model()

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":

        if form.is_valid():
            password = form.cleaned_data.get("password")
            try:
                token = Token.objects.get(key=password)
                if token is not None:
                    user = User.objects.get(id=token.user_id)
                    login(request, user)
                    return redirect("/")
            except:
                msg = 'Token incorrecto'
        else:
            msg = 'Error validating the form'

    return render(request, "registration/login.html", {"form": form, "msg": msg})

def logout_view(request):
    logout(request)
    return redirect("/login")