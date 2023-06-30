from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import coilStatus, coilType, coilProvider, coil, sku_Type, SKU, order, line, inventoryLocation, labelStatus, label


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
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
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

class CreateCoilForm(forms.Form):
    numrollo = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    boxNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    notDelivered = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_labelStatus_id = MyModelChoiceField(queryset=labelStatus.objects.all())
    FK_inventoryLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    FK_sku_id = ChoiceField(queryset=SKU.objects.all())
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())
    FK_coilType_id = MyModelChoiceField(queryset=coilType.objects.all())
    FK_coilProvider_id = MyModelChoiceField(queryset=coilProvider.objects.all())

class UpdateCoilForm(forms.ModelForm):
    numrollo = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    boxNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())

    class Meta:
        model = coil
        fields = 'numrollo', 'boxNumber', 'purchaseOrder', 'FK_coilStatus_id'


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

CHOICES =(
    ("abierta", "abierta"),
    ("cerrada", "cerrada")
)
class OrderForm(forms.ModelForm):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    status = forms.ChoiceField(choices=CHOICES)
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

class FilterCoilForm(forms.Form):
    boxNumber = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form"}))

class DeleteLabelForm(forms.Form):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class FilterLabelForm(forms.Form):
    uniqueid = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form"}))
    FK_labelStatus_id = MyModelChoiceField(queryset=labelStatus.objects.all(), required=False)

class UpdateLabelForm(forms.ModelForm):
    FK_inventoryLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    FK_labelStatus_id = MyModelChoiceField(queryset=labelStatus.objects.all())

    class Meta:
        model = label
        fields = 'FK_inventoryLocation_id', 'FK_labelStatus_id'
