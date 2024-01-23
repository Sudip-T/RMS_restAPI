from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny,SAFE_METHODS
from .serializers import *
from .models import *


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


class ProductView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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


class StoreRequestItemView(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    queryset = StoreRequestItem.objects.all()
    serializer_class = StoreRequestItemSerializer