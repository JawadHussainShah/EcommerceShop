from django.contrib import admin
from .models import Product,Category,Orders,EmailVerification
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'price','description', 'image','category']

@admin.register(Category)
class CategAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','quantity','price','adress','phone','date','product','customer','status']

@admin.register(EmailVerification)
class emailAdmin(admin.ModelAdmin):
    list_display = ['user','verify']