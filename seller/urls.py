
from django.urls import path
from .views import *

urlpatterns = [
    path('SLogin/',SLogin,name='SLogin'),
    path('SRegister/',SRegister,name='SRegister'),
    path('Slogout/',Slogout,name='Slogout'),
    path('Sindex/',Sindex,name='Sindex'),
    path('Scatpro/<int:id>',Scatpro,name='Scatpro'),
    path('orders/',orders,name='orders'),
    
 
    
]
