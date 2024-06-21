from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *



class MyModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class StatusChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.status

class ChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.sku

class OLChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.uniqueid

class SkuChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.description

class CoilChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"No. Caja: {obj.boxNumber} - SKU: {obj.sku}"

class CoilChoiceFieldFilter(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"No. Caja: {obj.boxNumber} - SKU: {obj.sku} Rango: {obj.initNumber} - {obj.finishNumber}"


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
    initNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    finishNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    numrollo = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    boxNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    notDelivered = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    unit = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    orderUniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_labelStatus_id = MyModelChoiceField(queryset=labelStatus.objects.all())
    FK_inventoryLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    FK_sku_id = SkuChoiceField(queryset=sku_Type.objects.all())
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())
    FK_coilType_id = MyModelChoiceField(queryset=coilType.objects.all())
    FK_coilProvider_id = MyModelChoiceField(queryset=coilProvider.objects.all())

class UpdateCoilForm(forms.ModelForm):
    numrollo = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    boxNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    unit = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    orderUniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    FK_sku_id = SkuChoiceField(queryset=sku_Type.objects.all())
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())

    class Meta:
        model = coil
        fields = 'numrollo', 'boxNumber', 'purchaseOrder', 'FK_coilStatus_id', 'unit', 'FK_sku_id','orderUniqueid'


class SkuTypeForm(forms.Form):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))

class SkuForm(forms.ModelForm):
    sku = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form"}))
    bts = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    cap = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    percentage_Alcohol = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    Fk_sku_type_id = MyModelChoiceField(queryset=sku_Type.objects.all())

    class Meta:
        model = SKU
        fields = 'sku', 'description', 'Fk_sku_type_id', 'bts', 'cap', 'percentage_Alcohol'

CHOICES =(
    ("abierta", "abierta"),
    ("cerrada", "cerrada")
)
class OrderForm(forms.ModelForm):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    lot = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    finish_date = forms.DateTimeField(help_text='End Date Time', required=False)
    finish_date.widget.attrs.update({
        'class': 'datetimepicker',
        'size': 14,
    })
    status = forms.ChoiceField(choices=CHOICES)
    FK_sku_id = SkuChoiceField(queryset=SKU.objects.all())

    class Meta:
        model = order
        fields = ('uniqueid', 'FK_sku_id', 'status', 'lot', 'finish_date')
        widgets = {
            'finish_date': forms.DateTimeInput(attrs={'class': 'datetimepicker'}),
        }

class LineForm(forms.Form):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class RequestStatusForm(forms.Form):
    status = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class AssignOrderForm(forms.Form):
    FK_order_id = OLChoiceField(queryset=order.objects.all())
    FK_line_id = OLChoiceField(queryset=line.objects.all())

class FilterCoilForm(forms.Form):
    boxNumber = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form"}))
    purchaseOrder = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class DeleteLabelForm(forms.Form):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))

class FilterLabelForm(forms.Form):
    uniqueid = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form"}))
    coil = CoilChoiceFieldFilter(queryset=coil.objects.all(), required=False)

class UpdateLabelForm(forms.ModelForm):
    FK_inventoryLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    FK_labelStatus_id = MyModelChoiceField(queryset=labelStatus.objects.all())

    class Meta:
        model = label
        fields = 'FK_inventoryLocation_id', 'FK_labelStatus_id'

class LabelInitForm(forms.Form):
    brand = MyModelChoiceField(queryset=sku_Type.objects.all())
    ministrationNumber = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    supplier = MyModelChoiceField(queryset=coilProvider.objects.all())

class ZipForm(forms.ModelForm):
    brand_name = MyModelChoiceField(queryset=sku_Type.objects.all())
    class Meta:
        model = zip_file_parent
        fields = ['password', 'ministration_number', 'brand_name', 'route']
        widgets = {
            'ministration_number': forms.TextInput(attrs={"class": "form"}),
            'password': forms.TextInput(attrs={"class": "form"}),
            'route': forms.FileInput(attrs={"accept": ".zip"})
        }

class CoilRequestForm(forms.ModelForm):
    FK_coil_id = CoilChoiceField(queryset=coil.objects.all())
    FK_order_id = OLChoiceField(queryset=order.objects.all())
    Fk_source_invLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    Fk_destination_invLocation_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    FK_coil_request_status_id = StatusChoiceField(queryset=coil_request_status.objects.all())

    class Meta:
        model = coil_request
        fields = 'FK_coil_id', 'FK_order_id', 'Fk_source_invLocation_id', 'Fk_destination_invLocation_id', 'FK_coil_request_status_id'

class CoilRequestFilter(forms.Form):
    Fk_coil_request_status = StatusChoiceField(queryset=coil_request_status.objects.all())

CHOICESBOOLEAN =(
    (True, "SI"),
    (False, "NO")
)

class CoilTraceForm(forms.ModelForm):
    FK_coil_id = CoilChoiceField(queryset=coil.objects.all())
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())
    FK_coilType_id = MyModelChoiceField(queryset=coilType.objects.all())
    FK_coilProvider_id = MyModelChoiceField(queryset=coilProvider.objects.all())
    FK_order_id = OLChoiceField(queryset=order.objects.all())
    FK_inventory_id = MyModelChoiceField(queryset=inventoryLocation.objects.all())
    initLabel = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
    IsUsed = forms.ChoiceField(choices=CHOICESBOOLEAN)

    class Meta:
        model = coilTrace
        fields = 'FK_coil_id', 'FK_coilStatus_id', 'FK_coilType_id', 'FK_coilProvider_id', 'FK_order_id', 'FK_inventory_id', 'initLabel', 'IsUsed'


class UpdateCoilTraceForm(forms.ModelForm):
    FK_coil_id = CoilChoiceField(queryset=coil.objects.all())
    FK_coilStatus_id = MyModelChoiceField(queryset=coilStatus.objects.all())
    FK_coilType_id = MyModelChoiceField(queryset=coilType.objects.all())
    FK_order_id = OLChoiceField(queryset=order.objects.all())

    class Meta:
        model = coilTrace
        fields = 'FK_coil_id', 'FK_coilStatus_id', 'FK_coilType_id', 'FK_order_id'

class orderForm2(forms.Form):
    uniqueid = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))


class LotSelectionForm(forms.Form):
    lote = forms.ModelChoiceField(queryset=lot.objects.none(), empty_label="Seleccione un lote")
    order_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super(LotSelectionForm, self).__init__(*args, **kwargs)
        if queryset is not None:
            self.fields['lote'].queryset = queryset
            self.fields['lote'].choices = [(x.id, x.lot) for x in queryset]

class CoilSelectionForm(forms.Form):
    selected_coils = forms.ModelMultipleChoiceField(queryset=coil.objects.all(), widget=forms.CheckboxSelectMultiple)

class CreateCoilFormv2(forms.Form):
    ordenproduccion = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form"}))
