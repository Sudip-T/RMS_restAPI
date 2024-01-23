from rest_framework import serializers
from .models import *


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturn
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturnItem
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRequest
        fields = '__all__'


class Serializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRequestItem
        fields = '__all__'