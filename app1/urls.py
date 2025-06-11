
from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name='index'),
    path('first/',first,name='first'),
    path('table/',table,name='table'),
    path('store_student/',store_student,name='student'),
    path('register/',register,name='register'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('catpro/<int:id>',cat_pro,name='catpro'),
    path('product_detail/<int:id>',product_detail,name='product_detail'),
    path('checkout/',checkout,name='checkout'),
    path('razorpay/',razorpayment,name='razorpay'),
    path('payment_handler/',payment_handler,name='payment_handler'),
    path('wish/',wish,name='wish'),
    path('wish/remove/<int:product_id>/', remove_from_wishlist, name='remove_from_wishlist'),
    path('wish/clear/', clear_wishlist, name='clear_wishlist'),
    path('cart_view/',cart_view,name='cart_view'),
    path('add_qty/<int:id>',add_qty,name='add_qty'),
    path('minus_qty/<int:id>',minus_qty,name='minus_qty'),
    path('cart/remove/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove_all/', remove_all_from_cart, name='remove_all_from_cart'),
    path('orderhistory/',orderhistory,name='orderhistory'),
    path('single_invoice/',single_invoice,name='single_invoice'),
    
    
    
    
    
]
