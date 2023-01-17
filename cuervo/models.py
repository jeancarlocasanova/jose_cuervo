from django.db import models
from django.conf import settings

# Create your models here.
class inventoryLocation(models.Model):
    name = models.CharField(max_length=50)
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

class coil(models.Model):
    uniqueid = models.CharField(max_length=20)
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.CASCADE, null=False, help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.CASCADE, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.CASCADE, null=False, help_text='Linked Coil Provider')
    last_update = models.DateTimeField(auto_now_add=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=False, help_text='Linked User' )

class label(models.Model):
    uniqueid = models.CharField(max_length=20)
    FK_coil_id = models.ForeignKey(coil, on_delete=models.CASCADE, null=False, help_text='Linked Coil')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.CASCADE, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.CASCADE, null=False, help_text='Linked Inventory Location')
    last_update = models.DateTimeField(auto_now_add=True, null=False)
    last_edit_user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=False, help_text='Linked User')

class labelTrace(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    FK_label_id = models.ForeignKey(label,on_delete=models.CASCADE, null=False, help_text='Linked Label')
    FK_labelStatus_id = models.ForeignKey(labelStatus, on_delete=models.CASCADE, null=False, help_text='Linked Label Status')
    FK_inventoryLocation_id = models.ForeignKey(inventoryLocation, on_delete=models.CASCADE, null=False, help_text='Linked Inventory Location')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, help_text='Linked User')

class coilTrace(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, null=False)
    FK_coil_id = models.ForeignKey(coil, on_delete=models.CASCADE, null=False, help_text='Linked Coil')
    FK_coilStatus_id = models.ForeignKey(coilStatus, on_delete=models.CASCADE, null=False, help_text='Linked Coil Status')
    FK_coilType_id = models.ForeignKey(coilType, on_delete=models.CASCADE, null=False, help_text='Linked Coil Type')
    FK_coilProvider_id = models.ForeignKey(coilProvider, on_delete=models.CASCADE, null=False, help_text='Linked Coil Provider')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, help_text='Linked User')





