from distutils.command.upload import upload
from itertools import product
from lib2to3.pgen2.grammar import opmap
from locale import currency
from msilib.schema import Class
from pydoc import ModuleScanner
from re import M
from time import time
from turtle import title
from django.db import models
from Buyer.models import Customer

# Create your models here.

class Category(models.Model):
    title=models.CharField(max_length=255)
    class Meta:
        db_table='Category'

class product_det(models.Model):
    Product_image=models.ImageField(upload_to="Product_image")
    Product_Name=models.CharField(max_length=30)
    seller_id=models.CharField(max_length=2)
    Total_quantity=models.IntegerField()
    date=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    price=models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    currency_type=models.CharField(max_length=10)
    Active=models.BooleanField(default=False)
    Category=models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    user=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    class Meta:
        db_table='Product_det'

class Cart(models.Model):
    product_id=models.ForeignKey(product_det,on_delete=models.DO_NOTHING)
    Customer_id=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    data=models.DateField(auto_now_add=True)
    time=models.TimeField(auto_now_add=True)
    class Meta:
        db_table='Cart'

class tag_pro(models.Model):
    t_products=models.TextField(max_length=500)
    product_id=models.ForeignKey(product_det,on_delete=models.DO_NOTHING)
    class Meta:
        db_table='tag_product'





