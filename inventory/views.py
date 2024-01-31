from .models import *
from .serializers import *
from rest_framework import status
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,SAFE_METHODS



class CategoryView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SupplierView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class StockItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

# todo : automatic update of stock item when purchase order is made or is returned
class PurchaseOrderView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = PurchaseOrder.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetPurchaseOrderSerializer
        return PurchaseOrderSerializer

    def create(self, request, *args, **kwargs):
        purchase_order_items = request.data.get('purchase_order_items')
        discount_rate = request.data.get('discount_rate')
        vat_rate = request.data.get('vat_rate')
        if not type(purchase_order_items) == list or not purchase_order_items:
            return Response({'error':'purchase_order_items must be a list or cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        sub_total = 0

        purchase_serializer =  PurchaseOrderSerializer(data=request.data)
        purchase_serializer.is_valid(raise_exception=True)
        purchase_order = purchase_serializer.save()

        for item in purchase_order_items:
            item['purchase_order'] = purchase_order.id
            purchase_item_serializer = PurchaseOrderItemSerializer(data=item)
            if not purchase_item_serializer.is_valid():
                PurchaseOrder.objects.get(id=purchase_order.id).delete()
                return Response({'error':purchase_item_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            item_total = item['purchase_quantity'] * item['unit_price']
            sub_total += item_total
            purchase_item_serializer.save()

        purchase_order.subtotal = sub_total

        if discount_rate:
            discount_amt = (sub_total*discount_rate)/100
            sub_total -= discount_amt
            purchase_order.discount_amt = discount_amt
        
        if vat_rate:
            vat_amt = (sub_total*vat_rate)/100
            purchase_order.vat_amt = vat_amt
            purchase_order.purchase_total = sub_total + vat_amt
            purchase_order.save()

        return Response({'msg':'purchase order created','data': purchase_serializer.data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        purchase_order_items = request.data.get('purchase_order_items')
        discount_rate = request.data.get('discount_rate')
        vat_rate = request.data.get('vat_rate')
        if not type(purchase_order_items) == list or not purchase_order_items:
            return Response({'error':'purchase_order_items must be a list or cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        sub_total = 0

        purchase_serializer =  PurchaseOrderSerializer(instance, data=request.data)
        purchase_serializer.is_valid(raise_exception=True)
        purchase_order = purchase_serializer.save()

        id_list = [instance.id for instance in instance.purchase_order_item.all()]
        req_id_list = []

        for item in purchase_order_items:
            item['purchase_order'] = instance.id
            if ('id' in item) and (item['id'] not in id_list):
                return Response({'purchase_order_items':f'Invalid pk \"{item["id"]}\" - object does not exist.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            elif ('id' in item) and (item['id'] in id_list):
                req_id_list.append(item['id'])
                item_instance = PurchaseOrderItem.objects.get(id=item['id'])
                serializer = PurchaseOrderItemSerializer(item_instance, data=item)
            else:
                serializer = PurchaseOrderItemSerializer(data=item)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            order_item = serializer.save()
            sub_total += order_item.purchase_item_total

        purchase_order.subtotal = sub_total

        if len(req_id_list) < len(id_list):
            for i in id_list:
                if i not in req_id_list:
                    PurchaseOrderItem.objects.get(id=i).delete()

        if discount_rate:
            discount_amt = (sub_total*discount_rate)/100
            sub_total -= discount_amt
            purchase_order.discount_amt = discount_amt
        
        if vat_rate:
            vat_amt = (sub_total*vat_rate)/100
            purchase_order.vat_amt = vat_amt
            purchase_order.purchase_total = sub_total + vat_amt
            purchase_order.save()
        return Response({'msg':'purchase order updated','data': purchase_serializer.data}, status=status.HTTP_200_OK)


class PurchaseOrderItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer


class PurchaseReturnView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = PurchaseReturn.objects.all()
    serializer_class = PurchaseReturnSerializer

    def create(self, request, *args, **kwargs):

        def is_list_of_dicts(variable):
            return isinstance(variable, list) and all(isinstance(item, dict) for item in variable)

        return_items = request.data.get('return_items')

        if not is_list_of_dicts(return_items) or not return_items:
            return Response({"error":"return_items can't be empty or must be a list of dictionaries"}, status=status.HTTP_400_BAD_REQUEST)

        purchase_serializer =  PurchaseReturnSerializer(data=request.data)
        purchase_serializer.is_valid(raise_exception=True)
        purchase_return = purchase_serializer.save()

        for item in return_items:
            item['purchase_return'] = purchase_return.id
            purchase_return_serializer = PurchaseReturnItemSerializer(data=item)
            if not purchase_return_serializer.is_valid():
                PurchaseReturn.objects.get(id=purchase_return.id).delete()
                return Response({'error':purchase_return_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            purchase_return_serializer.save()

        return Response({'msg':'purchase return created','data': purchase_serializer.data}, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):

        def is_list_of_dicts(variable):
            return isinstance(variable, list) and all(isinstance(item, dict) for item in variable)

        instance = self.get_object()
        return_items = request.data.get('return_items')

        if not is_list_of_dicts(return_items) or not return_items:
            return Response({"error":"return_items can't be empty or must be a list of dictionaries"}, status=status.HTTP_400_BAD_REQUEST)

        purchase_serializer =  PurchaseReturnSerializer(instance, data=request.data)
        purchase_serializer.is_valid(raise_exception=True)
        purchase_serializer.save()

        id_list = [instance.id for instance in instance.purchase_return_item.all()]
        req_id_list = []

        for item in return_items:
            item['purchase_return'] = instance.id
            if ('id' in item) and (item['id'] not in id_list):
                return Response({'return_items':f'Invalid pk \"{item["id"]}\" - object does not exist.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            elif ('id' in item) and (item['id'] in id_list):
                req_id_list.append(item['id'])
                item_instance = PurchaseReturnItem.objects.get(id=item['id'])
                serializer = PurchaseReturnItemSerializer(item_instance, data=item)
            else:
                serializer = PurchaseReturnItemSerializer(data=item)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

        if len(req_id_list) < len(id_list):
            for i in id_list:
                if i not in req_id_list:
                    PurchaseReturnItem.objects.get(id=i).delete()

        return Response({'msg':'purchase update successfull','data': purchase_serializer.data}, status=status.HTTP_201_CREATED)


class PurchaseReturnItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = PurchaseReturnItem.objects.all()
    serializer_class = PurchaseReturnItemSerializer
    

class StoreRequestView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StoreRequest.objects.all()
    serializer_class = StoreRequestSerializer

    # def get_queryset(self):
    #     queryset = self.queryset.filter(store_request_status='New')
    #     return queryset

    # def get_serializer_class(self):
    #     if self.request.method in SAFE_METHODS:
    #         return GetStoreRequestSerializer
    #     return StoreRequestSerializer


    def create(self, request, *args, **kwargs):
        request_items = request.data.get('store_request_items')
        if not type(request_items) == list or not request_items:
            return Response({'error':'store_request_items must be list or cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Creating the StoreRequest instance
        store_request_serializer = StoreRequestSerializer(data=request.data)
        store_request_serializer.is_valid(raise_exception=True)
        sr_data = store_request_serializer.save()
 
        # Creating StoreRequestItem instances
        for item in request_items:
            item['store_request'] = sr_data.id
            serializer = StoreRequestItemSerializer(data=item)
            if not serializer.is_valid():
                StoreRequest.objects.get(id=sr_data.id).delete()
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

        return Response({'msg':'store request created','data': store_request_serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):                       
        instance = self.get_object()
        request_items = request.data.get('store_request_items')
        if not type(request_items) == list or not request_items:
            return Response({'error':'store_request_items must be list or cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Updating the StoreRequest instance
        store_request_serializer = StoreRequestSerializer(instance,data=request.data)
        store_request_serializer.is_valid(raise_exception=True)
        store_request_serializer.save()

        id_list = [instance.id for instance in instance.StoreRequestItem.all()]
        req_id_list = []

        for item in request_items:
            item['store_request'] = instance.id
            if ('id' in item) and (item['id'] not in id_list):
                return Response({'store_request_items':f'Invalid pk \"{item["id"]}\" - object does not exist.'}, 
                                status=status.HTTP_400_BAD_REQUEST)
            elif ('id' in item) and (item['id'] in id_list):
                req_id_list.append(item['id'])
                item_instance = StoreRequestItem.objects.get(id=item['id'])
                serializer = StoreRequestItemSerializer(item_instance, data=item)
            else:
                serializer = StoreRequestItemSerializer(data=item)
            
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()

        # delete existing particular storerequestitem when not present in put request
        if len(req_id_list) < len(id_list):
            for i in id_list:
                if i not in req_id_list:
                    StoreRequestItem.objects.get(id=i).delete()

        return Response({'msg':'store request updated','data': store_request_serializer.data}, status=status.HTTP_200_OK)


#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         instance_itemsid = [instance.id for instance in instance.requested_products.all()]
#         for i in range(len(instance_itemsid)):
#             StoreRequestItem.objects.get(id=instance_itemsid[i]).delete()
#         return super().destroy(request, *args, **kwargs)


class StoreRequestItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StoreRequestItem.objects.all()
    serializer_class = StoreRequestItemSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetStoreRequestItemSerializer
        return StoreRequestItemSerializer