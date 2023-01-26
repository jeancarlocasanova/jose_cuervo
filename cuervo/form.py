from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

class SignUpForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )),
    password1 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class InventoryLocationForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class LabelStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class CoilStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class CoilTypeForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class CoilProviderForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))