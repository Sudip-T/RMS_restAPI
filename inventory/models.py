from django.db import models
from employee.models import Employee


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,related_name='products')

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_order')
    purchase_item = models.ForeignKey('PurchaseOrderItem', on_delete=models.CASCADE)
    purchase_note = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2)
    discount = models.DecimalField(max_digits=20,decimal_places=2)
    vat = models.DecimalField(max_digits=20,decimal_places=2)
    purchase_total = models.DecimalField(max_digits=20,decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.purchase_date
    

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, models.CASCADE, related_name='PurchaseOrderItem')
    purchase_item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='PurchaseOrderItem')
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    purchase_quantity = models.PositiveIntegerField()
    purchase_item_total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.purchase_item.name
    

class StoreRequest(models.Model):
    requested_products = models.ForeignKey('StoreRequestItem', on_delete=models.CASCADE)
    store_request_status = models.BooleanField(default=False)
    is_collected = models.BooleanField(default=False)
    collection_date = models.DateTimeField(auto_now=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    collected_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='collected_store_requests')
    requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='requested_store_requests')

    def __str__(self):
        return
    

class StoreRequestItem(models.Model):
    requested_item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_reuqest_item')
    requested_quantity = models.PositiveIntegerField()

    def __str__(self):
        return
    

class PurchaseReturn(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_return')
    returned_items = models.ForeignKey('PurchaseReturnItem',on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    collectedby_supplier = models.BooleanField(default=False)
    collection_date = models.DateTimeField(auto_now=True)
    return_reasons = models.TextField(blank=True, null=True)

    def __str__(self):
        return
    

class PurchaseReturnItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_return_item')
    purchase_items = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE, related_name='purchase_return_item')
    returned_quantity = models.PositiveIntegerField()

    def __str__(self):
        return