from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
# Tabel for Products...
# for category
class Category(models.Model):
    name = models.CharField(max_length=30)

    @staticmethod
    def get_all_category():
        return Category.objects.all()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_all_products():
        return Product.objects.all()
    
    def __str__(self):
        return self.name

class Orders(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    adress = models.CharField(max_length=50,default='',blank=True)
    phone = models.CharField(max_length=50,default='',blank=True)
    date = models.DateField(default=datetime.today)
    status = models.BooleanField(default=False)

#For Email Verification
class EmailVerification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True)
    verify = models.BooleanField(default=False)