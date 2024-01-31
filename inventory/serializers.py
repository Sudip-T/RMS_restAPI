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


class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderItem
        fields = '__all__'


class GetPurchaseOrderSerializer(serializers.ModelSerializer):
    purchase_order_items = PurchaseOrderItemSerializer(read_only=True, 
                            many=True, source='purchase_order_item')
    supplier = SupplierSerializer()

    class Meta:
        model = PurchaseOrder
        fields = '__all__'


class PurchaseOrderSerializer(serializers.ModelSerializer):
    purchase_order_items = PurchaseOrderItemSerializer(many=True, 
                    read_only=True, source='purchase_order_item')

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    # def validate(self, data):
    #     purchase_order_item_data = data.get('purchase_order_item')

    #     if not purchase_order_item_data or not isinstance(purchase_order_item_data, list):
    #         raise serializers.ValidationError('purchase_order_item must be a list of dictionaries.')

    #     if len(purchase_order_item_data) < 1:
    #         raise serializers.ValidationError('At least one purchase_order_item must be provided.')

    #     return data

    # def create(self, validated_data):
    #     purchase_order_items = validated_data.pop('purchase_order_item')
    #     purchase_order = PurchaseOrder.objects.create(**validated_data)

    #     for item_data in purchase_order_items:
    #         PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)

    #     return purchase_order
        # return super().create(validated_data)


class PurchaseReturnItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturnItem
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method in ['GET', 'LIST']:
            self.fields['purchase_item'] = PurchaseOrderItemSerializer()


class PurchaseReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseReturn
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('request') and self.context['request'].method in ['GET', 'LIST']:
            self.fields['return_items'] = PurchaseReturnItemSerializer(read_only=True, 
                            many=True, source='purchase_return_item')
            self.fields['supplier'] = SupplierSerializer()
    

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
    store_request_items = StoreRequestItemSerializer(many=True, 
                    read_only=True, source='StoreRequestItem')
    class Meta:
        model = StoreRequest
        fields = '__all__'


