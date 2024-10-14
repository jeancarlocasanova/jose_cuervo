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
    description = models.CharField(max_length=200)

class sku_SubType(models.Model):
    name = models.CharField(max_length=50)
    Fk_sku_type_id = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=True, help_text='Linked SKU Type')

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
    number = models.IntegerField(null=False, default=0)

class SKU(models.Model):
    sku = models.CharField(max_length=50)
    description = models.CharField(max_length=200,null=True)
    bts = models.CharField(max_length=12, default='',null=True)
    cap = models.CharField(max_length=10, default='',null=True)
    percentage_Alcohol = models.CharField(max_length=10, default='',null=True)
    asignacion = models.CharField(max_length=200, null=True)
    Fk_sku_subtype_id = models.ForeignKey(sku_SubType, on_delete=models.PROTECT, null=True, help_text='Linked SKU SubType')

class coil(models.Model):
    initNumber = models.CharField(max_length=200, null=False)
    finishNumber = models.CharField(max_length=200, null=False, help_text="Folio final")
    numrollo = models.IntegerField(default=1, null=False, help_text="Numero de Rollo")
    notDelivered = models.IntegerField(default=0)
    missing = models.IntegerField(null=False, default=0)
    delivered = models.IntegerField(null=False, default=0)
    boxNumber = models.IntegerField(null=False, default=1)
    purchaseOrder = models.CharField(default="NA", max_length=200, null=True)
    unit = models.CharField(default="PZ", max_length=200)
    orderUniqueid = models.CharField(max_length=200, help_text="Orden", null=True, default="")
    sku = models.CharField(max_length=200, null=True, help_text='Linked brand')
    Fk_sku_subtype_id = models.ForeignKey(sku_SubType, on_delete=models.PROTECT, null=True, help_text='Linked SKU SubType')
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.PROTECT, null=False, help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.PROTECT, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.CharField(max_length=200, null=True, help_text='Linked Coil Provider')
    last_update = models.DateTimeField(auto_now=True, null=False)
    qty_box = models.IntegerField(null=False, default=0)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User' )

class label(models.Model):
    uniqueid = models.CharField(max_length=999)
    url = models.CharField(max_length=999, default='')
    brand = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=True, help_text="SubMarca")
    ministrationNumber = models.CharField(max_length=100, null=True, default='')
    supplier = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=False, default=1)
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.PROTECT, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=True,
                                                help_text='Linked Inventory Location')
    last_update = models.DateTimeField(auto_now=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')
    expiration = models.DateTimeField(auto_now=False, null=True)

class labelTrace(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=False)
    FK_label_id = models.ForeignKey(label, on_delete=models.PROTECT, null=False, help_text='Linked Label')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.PROTECT, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=False, help_text='Linked Inventory Location')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')


class order(models.Model):
    uniqueid = models.CharField(max_length=30, null=True)
    FK_sku_id = models.ForeignKey(SKU, on_delete=models.PROTECT, null=True, help_text='Linked SKU')
    status = models.CharField(max_length=30, null=True)
    init_date = models.DateTimeField(auto_now=True, null=True)  # Set editable to False
    finish_date = models.DateTimeField(null=True)
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.PROTECT, null=True, help_text='Linked Inventory Location')
    coils = models.CharField(max_length=4000, null=True)


class lot(models.Model):
    lot = models.CharField(max_length=50, null=True)
    label_type = models.CharField(max_length=50, null=True)
    store = models.CharField(max_length=50, null=True)
    material = models.CharField(max_length=50, null=True)
    invoice_number = models.CharField(max_length=100, null=True)
    pieces_number = models.FloatField(max_length=100, null=True)
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.PROTECT, null=True, help_text='Linked Coil Provider')
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=True, help_text='Linked order')


class granel_lot(models.Model):
    granel_lot = models.CharField(max_length=50, null=True)
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=True, help_text='Linked order')

class GranelConsumptionDetail(models.Model):
    FK_order = models.ForeignKey(order, on_delete=models.CASCADE, help_text='Linked order')
    FK_granel_lot = models.ForeignKey(granel_lot, on_delete=models.CASCADE, help_text='Linked granel lot')
    FK_coil = models.ForeignKey(coil, on_delete=models.CASCADE, help_text='Linked coil')
    folio_inicial = models.CharField(max_length=200, null=True)
    folio_final = models.CharField(max_length=200, null=True)
    cantidad = models.IntegerField(null=True)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.FK_order.uniqueid} - {self.FK_granel_lot.granel_lot} - {self.FK_coil.numrollo}'


class coilTrace(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=False)
    FK_coil_id = models.ForeignKey(coil, on_delete=models.PROTECT, null=False, help_text='Linked Coil')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=False, help_text='Linked User')
    FK_order_id = models.ForeignKey(order, null=False, on_delete=models.PROTECT, default=0)
    initLabel = models.CharField(max_length=200, null=False)
    lastLabel = models.CharField(max_length=200, null=False)
    total_label = models.IntegerField(null=False, default=0)

class order_Exec(models.Model):
    FK_order_id = models.OneToOneField(order, on_delete=models.PROTECT, null=False, help_text='Linked Order')
    FK_line_id = models.OneToOneField(line, on_delete=models.PROTECT, null=False, help_text='Linked Line')

class order_Label(models.Model):
    FK_label_id = models.ForeignKey(label, on_delete=models.PROTECT, null=False, help_text="Linked Label")
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=False, help_text='Linked Order')

class coil_request_status(models.Model):
    status = models.CharField(max_length=50, null=False)

class coil_request(models.Model):
    FK_order_id = models.ForeignKey(order, on_delete=models.PROTECT, null=True, help_text="Linked Order")
    requested_coils = models.CharField(max_length=4000, null=True)
    request_date = models.DateTimeField(auto_now=True, null=True)
    FK_coil_request_status_id = models.ForeignKey(coil_request_status, on_delete=models.PROTECT, null=True, help_text="Linked Coil Request Status")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name='created_requests', help_text='Created By User')
    accepted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, related_name='accepted_requests', help_text='Accepted By User')
    total_number = models.IntegerField(null=True)

class init_label(models.Model):
    uniqueid = models.CharField(max_length=999)
    url = models.CharField(max_length=999, default='', unique=True)
    brand = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=False, related_name='destination', help_text="SubMarca", default=1)
    file_name = models.CharField(default='', max_length=200)
    ministrationNumber = models.CharField(max_length=100, null=False, default='')
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

class zip_file_parent(models.Model):
    file_name_parent = models.CharField(max_length=200, default='')
    processed = models.BooleanField(null=False, default=False)
    ministration_number = models.CharField(max_length=100, null=False, default='')
    brand_name = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=False, default=1)
    password = models.CharField(max_length=200, null=False, default='')
    update_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True)
    num_files = models.IntegerField(null=False, default=0)
    num_processed_files = models.IntegerField(null=False, default=0)
    seen = models.BooleanField(null=False, default=False)

    def __str__(self):
        return self.file_name_parent


class zip_file_child(models.Model):
    file_name = models.CharField(max_length=100)
    ministration_number = models.CharField(max_length=100, null=False, default='')
    brand_name = models.ForeignKey(sku_Type, on_delete=models.PROTECT, null=False, default=1)
    seen = models.BooleanField(null=False, default=False)
    update_date = models.DateTimeField(auto_now_add=True)
    processed_date = models.DateTimeField(null=True)
    parent = models.ForeignKey(zip_file_parent, on_delete=models.PROTECT, null=True)

class log_files(models.Model):
    file_name = models.CharField(max_length=200)
    comment = models.CharField(max_length=300)
    FK_zip_child = models.ForeignKey(zip_file_child, on_delete=models.PROTECT, null=True)
