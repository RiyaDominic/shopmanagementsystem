from django.db import models
from products.models import Products
from django.contrib.auth.models import User

# Create your models here.

class BillCalculations(models.Model):
    
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.CharField(max_length=11)
    BillId = models.IntegerField(blank=True,null=True)
    completed = models.BooleanField(default=False,null=True)

class BillFinal(models.Model):
    quantity = models.IntegerField(blank=True,null=True)
    toatalprice = models.IntegerField(blank=True,null=True)
    tax = models.IntegerField(blank=True,null=True)
    
class Cart(models.Model):
    
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    itemcount = models.CharField(max_length=255)
    house = models.CharField(max_length=255,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)
    area = models.CharField(max_length=255,null=True,blank=True)
    landmark = models.CharField(max_length=255,null=True,blank=True)
    paymentMethod = models.CharField(max_length=255,null=True,blank=True)
    orderId = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True,default="cart")

    
    