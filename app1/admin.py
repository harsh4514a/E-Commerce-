from django.contrib import admin

from.models import *


# Register your models here.
class Stu_(admin.ModelAdmin):
    list_display= ['id','name','email']
    

admin.site.register(Student,Stu_)
class Cat_(admin.ModelAdmin):
    list_display= ['id','name','image']
    

admin.site.register(Category,Cat_)

class Reg_(admin.ModelAdmin):
    list_display= ['id','name','email','mob','add','password']
    

admin.site.register(Registration,Reg_)

class Pro_(admin.ModelAdmin):
    list_display= ["id","name","price","image","added_by","category","stock"]

admin.site.register(Product,Pro_)

class Order_(admin.ModelAdmin):
    list_display= ["id","user","date_time","payment_mode","transaction_id","total_amount"]

admin.site.register(Order,Order_)

class Wishlist_(admin.ModelAdmin):
    list_display= ["id","pro","user"]

admin.site.register(wishlist,Wishlist_)

class Cart_(admin.ModelAdmin):
    list_display = ["id","pro","user","qty","total_amount","status"]
    
admin.site.register(Cart,Cart_)
