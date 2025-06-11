from django.contrib import admin
from .models import * 

# Register your models here.

class SellerR_(admin.ModelAdmin):
    list_display = ["id","name","email","add","mob","password"]
    
admin.site.register(SellerRegistration ,SellerR_)