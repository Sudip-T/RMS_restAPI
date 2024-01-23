from django.contrib import admin
from .models import *


admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderItem)
admin.site.register(PurchaseReturn)
admin.site.register(PurchaseReturnItem)
admin.site.register(StoreRequest)
admin.site.register(StoreRequestItem)
