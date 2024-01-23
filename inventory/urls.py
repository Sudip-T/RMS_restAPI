from django.urls import path,include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'category',CategoryView,basename='category')
router.register(r'supplier',SupplierView,basename='supplier')
router.register(r'product',ProductView,basename='product')
router.register(r'purchase-order',PurchaseOrderView,basename='purchase_order')
router.register(r'purchase-order-item',PurchaseOrderItemView,basename='purchase_order_item')
router.register(r'purchase-return',PurchaseReturnView,basename='purchase_return')
router.register(r'purchase-return-item',PurchaseReturnItemView,basename='purchase_return_item')
router.register(r'store-request',StoreRequestView,basename='store_request')
router.register(r'store-requset-item',StoreRequestItemView,basename='store_requset_item')

urlpatterns = [
    path('inventory/', include(router.urls))
]

# urlpatterns = router.urls