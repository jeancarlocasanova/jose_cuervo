from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import inventoryLocation, labelStatus , coilStatus

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

class EditInventoryLocationForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

    class Meta:
        model = inventoryLocation
        fields = ['name', 'description']

class LabelStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class EditLabelStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

    class Meta:
        model = labelStatus
        fields = ['name', 'description']

class CoilStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class EditCoilStatusForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

    class Meta:
        model = coilStatus
        fields = ['name', 'description']