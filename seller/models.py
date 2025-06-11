from django.db import models

# Create your models here.

class SellerRegistration(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    add = models.TextField()
    mob = models.CharField(max_length=10)
    password = models.CharField(max_length=8)
    accept = models.BooleanField(default=False) 
    
    def __str__(self):
        return f"{self.name} -- {self.email}"
    
    class Meta:
        verbose_name_plural = "Seller Registration"