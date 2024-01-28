from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if self.context['request'].method in ['GET', 'LIST']:
    #         self.fields['category'] = CategorySerializer()


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


class PurchaseReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturn
        fields = '__all__'
    
    def create(self, validated_data):
        returned_items = validated_data.get('returned_items')
        data_list = []
        for i in returned_items:
            print(i)
        return super().create(validated_data)


class PurchaseReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturnItem
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context['request'].method in ['GET', 'LIST']:
            self.fields['purchase_item'] = PurchaseOrderItemSerializer()


class GetStoreRequestItemSerializer(serializers.ModelSerializer):
    requested_item = StockItemSerializer()
    class Meta:
        model = StoreRequestItem
        fields = '__all__'


class StoreRequestItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreRequestItem
        fields = '__all__'


class StoreRequestSerializer(serializers.ModelSerializer):
    store_request_items = StoreRequestItemSerializer(many=True, read_only=True, source='StoreRequestItem')
    class Meta:
        model = StoreRequest
        fields = '__all__'


# class StoreRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StoreRequest
#         fields = '__all__'

