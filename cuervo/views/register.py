from ..form import SignUpForm
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.shortcuts import render

User = get_user_model()

def register_token(request):
    msg = None
    success = False
    tokenMsg = None

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            try:
                userObj = User.objects.get(username=username)
            except:
                userObj = None

            if userObj is None:
                userObj = User.objects.create_user(username=username, password=raw_password)
                userObj.save()
                token = Token.objects.create(user=userObj)
                token.save()
                tokenMsg = token.key
                msg = 'Usuario creado - Inserta el siguiente Token en el Login: '
                success = True
            else:
                msg = 'Este Nombre de usuario ya existe'
        else:
            msg = 'A ocurrido un error'
            print(form.errors)
    else:
        form = SignUpForm()

    return render(request, "registration/register.html", {"form": form, "msg": msg, "success": success, "token": tokenMsg})
