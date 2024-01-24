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
    
    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetStoreRequestSerializer
        return StoreRequestSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.get('requested_products')
        data_list = []

        # Creating StoreRequestItem instances
        for item in data:
            serializer = StoreRequestItemSerializer(data=item)
            if serializer.is_valid():
                store_request_item = serializer.save()
                data_list.append(store_request_item.id)
            else:
                for i in range(len(data_list)):
                    StoreRequestItem.objects.get(id=data_list[i]).delete()
                return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Updating the request data with the IDs of created StoreRequestItem instances
        store_request_data = request.data.copy()
        store_request_data['requested_products'] = data_list

        # Creating the StoreRequest instance
        store_request_serializer = StoreRequestSerializer(data=store_request_data)
        store_request_serializer.is_valid(raise_exception=True)
        store_request_serializer.save()

        return Response({'results': store_request_serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data.get('requested_products')
        data_list = []

        # instance_itemsid = instance.requested_products.all()
        instance_itemsid = [instance.id for instance in instance.requested_products.all()]

        # Updating existing StoreRequestItem instances
        for i,item_data in enumerate(data):
            try:
                item_instance = instance.requested_products.get(id=instance_itemsid[i])
                serializer = StoreRequestItemSerializer(instance=item_instance, data=item_data, partial=True)
                serializer.is_valid(raise_exception=True)
                store_request_item = serializer.save()
                data_list.append(store_request_item.id)
            except Exception as e:
                error_data = {'requested_products':f'Invalid pk {item_data["requested_item"]} - object does not exist.'}
                return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        # Updating the request data with the IDs of updated StoreRequestItem instances
        store_request_data = request.data.copy()
        store_request_data['requested_products'] = data_list

        # Updating the StoreRequest instance
        store_request_serializer = StoreRequestSerializer(instance, data=store_request_data, partial=True)
        store_request_serializer.is_valid(raise_exception=True)
        store_request_serializer.save()

        return Response({'results': store_request_serializer.data}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_itemsid = [instance.id for instance in instance.requested_products.all()]
        for i in range(len(instance_itemsid)):
            StoreRequestItem.objects.get(id=instance_itemsid[i]).delete()
        return super().destroy(request, *args, **kwargs)


class StoreRequestItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StoreRequestItem.objects.all()
    serializer_class = StoreRequestItemSerializer

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return GetStoreRequestItemSerializer
        return StoreRequestItemSerializer