from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class inventoryLocation(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class line(models.Model):
    uniqueid = models.CharField(max_length=30)
class sku_Type(models.Model):
    name = models.CharField(max_length=50)
    subbrand = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=200)

class labelStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class coilStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

class coilType(models.Model):
    name = models.CharField(max_length=70)

class coilProvider(models.Model):
    name = models.CharField(max_length=70)

class SKU(models.Model):
    sku = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    bts = models.CharField(max_length=12, default='')
    cap = models.CharField(max_length=10, default='')
    percentage_Alcohol = models.CharField(max_length=10, default='')
    Fk_sku_type_id = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=False, help_text='Linked SKU Type')

class coil(models.Model):
    initNumber = models.CharField(max_length=200, null=False)
    finishNumber = models.CharField(max_length=200, null=False, help_text="Folio final")
    numrollo = models.IntegerField(default=1, null=False, help_text="Numero de Rollo")
    notDelivered = models.IntegerField(default=0)
    missing = models.IntegerField(null=False, default=0)
    delivered = models.IntegerField(null=False, default=0)
    boxNumber = models.IntegerField(null=False, default=1)
    purchaseOrder = models.CharField(default="NA", max_length=50)
    unit = models.CharField(default="P2", max_length=50)
    orderUniqueid = models.CharField(max_length=10, help_text="Orden", null=False, default="")
    FK_sku_id = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=True, help_text='Linked brand')
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.PROTECT, null=False, help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.PROTECT, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=False, help_text='Linked Coil Provider')
    last_update = models.DateTimeField(auto_now=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User' )

class label(models.Model):
    uniqueid = models.CharField(max_length=999)
    url = models.CharField(max_length=999, default='')
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.PROTECT, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=False, help_text='Linked Inventory Location')
    last_update = models.DateTimeField(auto_now=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')
    expiration = models.DateTimeField(auto_now=False, null=True)
    comment = models.CharField(max_length=999, null=True)

class labelTrace(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=False)
    FK_label_id = models.ForeignKey(label, on_delete=models.PROTECT, null=False, help_text='Linked Label')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.PROTECT, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=False, help_text='Linked Inventory Location')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')


class order(models.Model):
    uniqueid = models.CharField(max_length=30)
    status = models.CharField(max_length=30, default="abierta")
    lot = models.CharField(max_length=30, default='')
    init_date = models.DateTimeField(auto_now=True, null=False)  # Set editable to False
    finish_date = models.DateTimeField(null=True)
    coils = models.CharField(max_length=100, null=True)
    FK_sku_id = models.ForeignKey(SKU, on_delete=models.PROTECT, null=False, help_text='Linked SKU')

class coilTrace(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=False)
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.PROTECT, null=False, help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.PROTECT, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=False, help_text='Linked Coil Provider')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')
    FK_order_id = models.ForeignKey(order, null=False, on_delete=models.PROTECT, default=0)
    FK_inventory_id = models.ForeignKey(inventoryLocation, null=False, on_delete=models.PROTECT, default=0)
    initLabel = models.CharField(max_length=200, null=False)
    lastLabel = models.CharField(max_length=200, null=False)
    IsReturned = models.BooleanField(null=False, default=False)
    IsUsed = models.BooleanField(null=False, default=False)

class order_Exec(models.Model):
    FK_order_id = models.OneToOneField(order, on_delete=models.PROTECT, null=False, help_text='Linked Order')
    FK_line_id = models.OneToOneField(line, on_delete=models.PROTECT, null=False, help_text='Linked Line')

class order_Label(models.Model):
    FK_label_id = models.ForeignKey(label, on_delete=models.PROTECT, null=False, help_text="Linked Label")
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=False, help_text='Linked Order')

class coil_request_status(models.Model):
    status = models.CharField(max_length=50, null=False)

class coil_request(models.Model):
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')
    startingNumber = models.CharField(max_length=200, null=False)
    endingNumber = models.CharField(max_length=200, null=False)
    request_date = models.DateTimeField(auto_now=True, null=False)
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=False, help_text="Linked Order")
    Fk_source_invLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=False, related_name='source', help_text="Linked Source Inventory Location")
    Fk_destination_invLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=False,related_name='destination', help_text="Linked Destination Inventory Location")
    FK_coil_request_status_id = models.ForeignKey(coil_request_status, on_delete=models.PROTECT, null=False, help_text="Linked Coil Request Status")
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True,
                                       help_text='Linked User')

class init_label(models.Model):
    uniqueid = models.CharField(max_length=999, unique=True)
    url = models.CharField(max_length=999, default='')
    brand = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=False, related_name='destination', help_text="SubMarca", default=1)
    file_name = models.CharField(default='', max_length=200)
    ministrationNumber = models.CharField(max_length=100, null=False, default='')
    supplier = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=False, default=1)
    update_date = models.DateTimeField(auto_now=True, null=False)
    expiration = models.DateTimeField(auto_now=False, null=True)

class coilsInInventory(models.Model):
    initNumber = models.IntegerField(default=0, null=False, help_text="Folio Inicial")
    finishNumber = models.IntegerField(default=0, null=False, help_text="Folio final")
    numrollo = models.IntegerField(default=1, null=False, help_text="Numero de Rollo")
    notDelivered = models.IntegerField(default=0)
    missing = models.IntegerField(null=False, default=0)
    delivered = models.IntegerField(null=False, default=0)
    boxNumber = models.IntegerField(null=False, default=1)
    purchaseOrder = models.CharField(default="NA", max_length=50)
    unit = models.CharField(default="P2", max_length=50)
    orderUniqueid = models.CharField(max_length=10, help_text="Orden", null=False, default="")
    FK_sku_id = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=True, help_text='Linked brand')
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.PROTECT, null=False,
                                         help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.PROTECT, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=False,
                                           help_text='Linked Coil Provider')
    last_update = models.DateTimeField(auto_now=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False,
                                       help_text='Linked User')
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')

