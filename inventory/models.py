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
    

class StockItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT,related_name='products')

    def __str__(self):
        return self.name
    

class PurchaseOrder(models.Model):
    Supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_order')
    purchase_item = models.ForeignKey('PurchaseOrderItem', on_delete=models.CASCADE)
    purchase_note = models.TextField(blank=True, null=True)
    subtotal = models.DecimalField(max_digits=20,decimal_places=2)
    discount = models.DecimalField(max_digits=20,decimal_places=2, blank=True,null=True)
    vat = models.DecimalField(max_digits=20,decimal_places=2)
    purchase_total = models.DecimalField(max_digits=20,decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Supplier.name
    

class PurchaseOrderItem(models.Model):
    # purchase_order = models.ForeignKey(PurchaseOrder, models.CASCADE, related_name='PurchaseOrderItem')
    purchase_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='PurchaseOrderItem')
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    purchase_quantity = models.PositiveIntegerField()
    purchase_item_total = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.purchase_item.name
    

class StoreRequest(models.Model):
    STATUS = [
        ('New','New'),
        ('Approved','Approved')
    ]
    store_request_status = models.CharField(choices=STATUS, default='New', max_length=20)
    is_collected = models.BooleanField(default=False)
    collection_date = models.DateTimeField(blank=True, null=True)
    requested_date = models.DateTimeField(auto_now_add=True)
    collected_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='store_collected_by', blank=True, null=True)
    requested_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='store_requestedby')

    # todo : when store_request_status == 'Approved', update stock quantity automatically

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.collection_date and self.collected_by:
            self.is_collected = True
        super().save(*args, **kwargs)
    

class StoreRequestItem(models.Model):
    store_request = models.ForeignKey(StoreRequest,on_delete=models.CASCADE, related_name='StoreRequestItem')
    requested_item = models.ForeignKey(StockItem, on_delete=models.CASCADE, related_name='store_reuqest_item')
    requested_quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.requested_item.name
    

class PurchaseReturn(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='purchase_return')
    returned_items = models.ManyToManyField('PurchaseReturnItem')
    created_date = models.DateTimeField(auto_now_add=True)
    collectedby_supplier = models.BooleanField(default=False)
    collection_date = models.DateTimeField(auto_now=True)
    return_reasons = models.TextField(blank=True, null=True)

    # def __str__(self):
    #     return
    

class PurchaseReturnItem(models.Model):
    purchase_item = models.ForeignKey(PurchaseOrderItem,on_delete=models.CASCADE, related_name='purchase_return_item')
    returned_quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True)

    # def __str__(self):
    #     return

    def save(self, *args,**kwargs):
        self.unit_price = self.purchase_item.unit_price
        self.sub_total = self.unit_price * self.returned_quantity
        super().save(*args, **kwargs)