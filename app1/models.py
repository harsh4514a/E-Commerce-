from django.db import models
from seller.models import * 
# Create your models here.
#table create
class Student(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __str__(self):
        return self.email
    
class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category_image')
    
    def __str__(self):
        return self.name
        
class Registration(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    add = models.CharField(max_length=50)
    mob = models.CharField(max_length=50)
    password = models.CharField(max_length=8)
    
    
    def __str__(self):
        return self.email
    
class Product(models.Model):
    added_by = models.ForeignKey(SellerRegistration,on_delete=models.CASCADE,blank=True,null=True)
    
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='pro_img')
    description = models.TextField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name
    
    
STATUS = (
    ("Pending", "Pending"),
    ("Order Placed", "Order Placed"),
    ("On the way", "On the way"),
    ("Delivered", "Delivered"),
    
)       
class Cart(models.Model):
    pro = models.ForeignKey(Product,on_delete=models.CASCADE) 
    user = models.ForeignKey(Registration,on_delete=models.CASCADE) 
    qty = models.PositiveBigIntegerField()
    total_amount = models.PositiveIntegerField()
    order_id = models.PositiveBigIntegerField(default=0)
    ordered = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS,verbose_name="Order Status",default="Pending",max_length=20)
    
    
    def __str__(self):
        return f"{self.user} -{self.pro.name} - {self.qty} - {self.status}"  
    

class Order(models.Model):
    prods = models.ManyToManyField(Cart)
    user = models.ForeignKey(Registration,on_delete=models.CASCADE)   
    date_time = models.DateTimeField(auto_now=True)
    payment_mode = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100,blank=True,null=True)
    total_amount = models.PositiveIntegerField()
    add = models.TextField()
    mob = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6)
    ordered = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.user)
    
class wishlist(models.Model):
    pro = models.ForeignKey(Product,on_delete=models.CASCADE) 
    user = models.ForeignKey(Registration,on_delete=models.CASCADE)   
    
    
    def __str__(self):
        return str(self.user)
    

