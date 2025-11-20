from django.db import models

class Product(models.Model):
    category        = models.CharField(max_length=215, blank=True, null=True)
    descriptions    = models.TextField(max_length=215, blank=True, null=True)
    unit            = models.TextField(max_length=215, blank=True, null=True)
    qty             = models.IntegerField(default=0)
    costprice       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    sellprice       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    saleprice       = models.DecimalField(max_digits=10, decimal_places=2, default=0.00) 
    productpicture  = models.TextField(max_length=215, blank=True, null=True)
    alertstocks     = models.IntegerField(default=0)
    criticalstocks  = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    # def __str__(self):
    #     return f"Product object created at {self.created_at}, last updated at {self.updated_at}"