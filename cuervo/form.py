from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import coilStatus, coilType, coilProvider, coil, sku_Type, SKU, order, line


class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name
class ChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.sku

class OLChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.uniqueid


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

class CoilForm(forms.ModelForm):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())
    FK_coilType_id = MyModelChoiceField(queryset=coilType.objects.all())
    FK_coilProvider_id = MyModelChoiceField(queryset=coilProvider.objects.all())

    class Meta:
        model = coil
        fields = 'uniqueid', 'FK_coilStatus_id', 'FK_coilType_id', 'FK_coilProvider_id'

class SkuTypeForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class SkuForm(forms.ModelForm):
    sku = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))
    Fk_sku_type_id = MyModelChoiceField(queryset=sku_Type.objects.all())

    class Meta:
        model = SKU
        fields = 'sku', 'description', 'Fk_sku_type_id'

class OrderForm(forms.ModelForm):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_sku_id = ChoiceField(queryset=SKU.objects.all())

    class Meta:
        model = order
        fields = 'uniqueid', 'FK_sku_id'

class LineForm(forms.Form):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class RequestStatusForm(forms.Form):
    status = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class AssignOrderForm(forms.Form):
    FK_order_id = OLChoiceField(queryset=order.objects.all())
    FK_line_id = OLChoiceField(queryset=line.objects.all())
