from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,SAFE_METHODS
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status



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


class PurchaseOrderView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


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