from rest_framework import serializers
from cuervo.models import order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = order
        fields = ('uniqueid', 'status', 'FK_sku_id')