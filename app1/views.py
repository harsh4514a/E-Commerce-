from django.shortcuts import render , HttpResponse , redirect,get_object_or_404
from .models import *
import random
# Create your views here.


def demo(request):
    return HttpResponse("This is my first viwe.....")

def first(request):
    return render(request,'first.html')


def table(request):
    cat_data = Category.objects.all()
    print(cat_data)
    # a = ["hello","tegyh",7545,True]
    # for i in a:
    #     print(a)
    # for i in cat_data:
    #     print(i.id)
    #     print(i.name)
    #     print(i.image)
    return render(request,'table.html',{'Category':cat_data})

def store_student(request):
    if request.method == 'POST' and request.FILES:
        store_student = Category()
        store_student.name = request.POST['uname']
        store_student.image = request.POST['img']
        store_student.save()
        
    return render(request,'Student.html')

def register(request):
    if request.method =='POST':
        store_reg = Registration()
        store_reg.name = request.POST['name']
        store_reg.email = request.POST['email']
        store_reg.add = request.POST['add']
        store_reg.mob = request.POST['mob']
        store_reg.password = request.POST['password']
        store_reg.c_password = request.POST['c_password']
        
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password !=c_password:
            return render(request,'register.html',{'diff':"Enter confirm password same as password"})
                
        try:
            already_registered = Registration.objects.get(email = request.POST['email'])
            if already_registered:
                return render(request,'register.html',{'already_registered':"This email already registered"})
            
     
        except:
            store_reg.save()
            return render(request,'register.html',{'stored':"Registration succefull"})
       
            
                
        
    else:
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        try:
            register_data = Registration.objects.get(email = request.POST['email'])
            if request.POST['password'] == register_data.password:
                request.session["login"] = register_data.email
                return redirect('index')
            else:
                return render(request,'login.html',{'incorrect_Pass':"Please enter valid password .."})   
        except:
            return render(request,'login.html',{'incorrect_email':"Please enter valid email.."})   

    
    return render(request,'login.html')   

def index(request):
    cat_data = Category.objects.all()
    
    if 'login' in request.session:
        return render(request,"index.html",{'category':cat_data,'logged_in':True})

    else:
        return render(request,"index.html",{'category':cat_data})
        
def logout(request):
    del request.session['login']       
    return redirect("index")    

def cat_pro(request,id ):
    prod = Product.objects.filter(category = id)
    category = Category.objects.get(id=id)
    if 'login' in request.session:
        return render(request,"cat_pro.html",{'prod':prod,'logged_in':True, 'category_name': category.name})

    else:
        return render(request,'cat_pro.html',{'prod':prod, 'category_name': category.name}) 
    
def product_detail(request,id):
    product = Product.objects.get(id = id)
    category = product.category
    
    if 'login' in request.session:  
        logged_in = Registration.objects.get(email = request.session["login"])                 

        if 'buy' in request.POST:
            add_to_cart = Cart()
            add_to_cart.pro = product
            add_to_cart.user = logged_in
            add_to_cart.qty = request.POST['qty']
            add_to_cart.total_amount = int(request.POST['qty']) * product.price
            add_to_cart.save()
            product.stock -= int(request.POST['qty'])
            product.save()
            request.session["proid"] = id
            request.session["qty"] = request.POST['qty']
            request.session["amount"] = int(request.POST['qty']) * product.price
            return redirect("checkout")
            
        elif 'wish' in request.POST:             
            add_to_wishlist = wishlist()
            add_to_wishlist.pro = product
            add_to_wishlist.user = logged_in
            add_to_wishlist.save() 
            return render(request,'product.html',{'product':product, 'category': category,'logged_in':True}) 
             
        elif 'cart' in request.POST: 
            request.session['proid'] = id
            request.session['qty'] = request.POST["qty"]           
            add_to_cart = Cart()  
            add_to_cart.pro = product
            add_to_cart.user = logged_in
            add_to_cart.qty = request.POST["qty"]
            add_to_cart.total_amount = int(request.POST["qty"]) * product.price           
            add_to_cart.save()
            product.stock -= int(request.POST['qty'])
            product.save()
            return render(request,'product.html',{'product':product, 'category': category,'logged_in':True}) 
            
        else:
            return render(request,'product.html',{'product':product, 'category': category,'logged_in':True}) 
            
    else:
        if request.method == "POST":
            return redirect('login')     
        else:     
            return render(request,'product.html',{'product':product, 'category': category}) 
        


def checkout(request):
    
    if 'login' in request.session:
        logged_in_user=Registration.objects.get(email = request.session["login"])
        tempCart = Cart.objects.filter(ordered=False , user__email = request.session['login'])
        print(tempCart)
        if 'proid' not in request.session:
            return redirect('cart_view')
        pro = Product.objects.get(id = request.session['proid'])
        if request.method == 'POST':
            if request.POST["paymentvia"] == "cod":
                c = request.POST["city"]
                s = request.POST["state"]
                p = request.POST["pin"]
                if c or s or p:
                    if c:
                        if s:
                            if p:   
                                total_amount = 0
                                for item in tempCart:
                                    item_total = item.qty * item.pro.price
                                    total_amount += item_total 
                                                   
                                store_order = Order.objects.create(
                                    total_amount = total_amount,
                                    user = logged_in_user,
                                    payment_mode = request.POST['paymentvia'],
                                    transaction_id = str(random.randint(10**9,10**10-1)),
                                    add = request.POST["add"],
                                    mob = request.POST["mob"],
                                    city = request.POST["city"], 
                                    state =request.POST["state"],
                                    pin_code = request.POST["pin"],
                                    ordered = True
                                )
                                store_order.prods.add(*tempCart)
                                tempCart.update(ordered=True,status="Order Placed")
                                store_order.save()
                                pro.stock -= int(request.session["qty"])
                                pro.save()
                                order = get_object_or_404(Order,id=store_order.id)
                                param ={'order':order}
                                return render(request, 'invoice.html',param)
                            else:
                                return HttpResponse("<script>alert('Enter Pin Code');window.location.href='/checkout/';</script>")
                        else:
                            return HttpResponse("<script>alert('Enter State');window.location.href='/checkout/';</script>")
                    else:
                        return HttpResponse("<script>alert('Enter City');window.location.href='/checkout/';</script>")
                else:
                    return HttpResponse("<script>alert('Enter City, State, Zip Code');window.location.href='/checkout/';</script>")
            else:
                c = request.POST["city"]
                s = request.POST["state"]
                p = request.POST["pin"]
                if c or s or p:
                    if c:
                        if s:
                            if p:   
                                total_amount = 0
                                for item in tempCart:
                                    item_total = item.qty * item.pro.price
                                    total_amount += item_total    
                                request.session['total_amount'] = total_amount    
                                request.session['add'] = request.POST["add"]
                                request.session['mob'] = request.POST["mob"]
                                request.session['pin_code'] = request.POST["pin"]
                                request.session['city'] = request.POST["city"]
                                request.session['state'] = request.POST["state"]
                                request.session['country'] = request.POST["country"]
                                return redirect("razorpay")
                            else:
                                return HttpResponse("<script>alert('Enter Pin Code');window.location.href='/checkout/';</script>")
                        else:
                            return HttpResponse("<script>alert('Enter State');window.location.href='/checkout/';</script>")
                    else:
                        return HttpResponse("<script>alert('Enter City');window.location.href='/checkout/';</script>")
                else:
                    return HttpResponse("<script>alert('Add City, State & Zip Code');window.location.href='/checkout/';</script>")
                    

        else:
            
            return render(request,"checkout.html",{'logged_in':logged_in_user})

    else:
        return redirect("login")

import razorpay
from django.conf import settings
from django.http import *
from django.views.decorators.csrf import *
razorpay_client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))

def razorpayment(request):
    amount = request.session['total_amount'] * 100
    currency='INR'
    razorpay_order = razorpay_client.order.create(dict(amount = amount, currency = currency,payment_capture = '0'))
    return render(request,"razorpay.html",{"razorpay_merchant_key":settings.RAZORPAY_KEY_ID,
                                           "razorpay_amount":amount,"currency":currency,
                                           "razorpay_order_id":razorpay_order['id'],
                                           "callback_url":'http://127.0.0.1:8000/payment_handler/'})


@csrf_exempt
def payment_handler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '') 
            order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            param_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            # verify the payment signature.
            razorpay_client.utility.verify_payment_signature(param_dict)
            amount = request.session['total_amount'] * 100       
            razorpay_client.payment.capture(payment_id, amount)
            pro = Product.objects.get(id = request.session['proid'])
            logged_in_user=Registration.objects.get(email = request.session["login"])
            
            tempCart = Cart.objects.filter(ordered=False , user__email = request.session['login'])
            
            order_store = Order.objects.create(
                user = logged_in_user,
                payment_mode = 'online',
                transaction_id = payment_id,
                total_amount = request.session["total_amount"],
                add = request.session["add"],
                mob = request.session["mob"],
                pin_code = request.session["pin_code"],
                city = request.session["city"],
                state = request.session["state"],
                ordered=True
            )
            order_store.prods.add(*tempCart)
            tempCart.update(ordered=True,status="Order Placed")
            order_store.save()
            pro.stock -= int(request.session["qty"])
            pro.save()
            order = get_object_or_404(Order,id=order_store.id)
            param ={'order':order}
            return render(request, 'invoice.html',param) 
        except Exception as e:
            print(e,"erooorrrrrr")
            return HttpResponseBadRequest()
    else:
        return HttpResponseRedirect()
    
def wish(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session["login"])                 
        wishlist_data = wishlist.objects.filter(user = logged_in)
        total = 0
        for i in wishlist_data:
            total += i.pro.price
        return render(request,"wish.html",{'logged_in':True,'wishlist':wishlist_data,'total':total})

    else:
        return  redirect("login")

def remove_from_wishlist(request, product_id):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email=request.session["login"])
        try:
            item = wishlist.objects.get(user=logged_in, pro_id=product_id)
            item.delete()
        except wishlist.DoesNotExist:
            pass
        return redirect('wish')
    else:
        return redirect('login')

def clear_wishlist(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email=request.session["login"])
        wishlist.objects.filter(user=logged_in).delete()
        return redirect('wish')
    else:
        return redirect('login')
    
def cart_view(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email = request.session["login"])                         
        cart_data = Cart.objects.filter(user = logged_in,ordered=False)
        total = 0
        for i in cart_data:
            total += i.total_amount
        if 'outofstock' in request.session:
            del request.session['outofstock']
            return render(request,"cart.html",{'logged_in':True,'cartlist':cart_data,'total':total,'outofstock':'this product is out of stock'})
        else:   
             return render(request,"cart.html",{'logged_in':True,'cartlist':cart_data,'total':total})

    else:
        return redirect('login')
    
def add_qty(request,id):
    cart_row = Cart.objects.get(id=id)
    pro = Product.objects.get(id =cart_row.pro.id)
    if pro.stock <= 0:
        request.session["outofstock"] = True
        return redirect("cart_view")
    else:
        cart_row.qty += 1
        cart_row.total_amount += pro.price
        cart_row.save()
        pro.stock -= 1   
        pro.save()
        return redirect('cart_view')

def minus_qty(request,id):
    cart_data = Cart.objects.get(id =id)
    pro = Product.objects.get(id =cart_data.pro.id)
    if cart_data.qty <= 1 :
        cart_data.delete()
        return redirect("cart_view")
    else:
        cart_data.qty -= 1
        cart_data.total_amount -= pro.price
        cart_data.save()
        pro.stock += 1
        pro.save()
        return redirect('cart_view')
       
def remove_all_from_cart(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email=request.session["login"])
        cart_data = Cart.objects.filter(user=logged_in)
        for i in cart_data:
            pro = Product.objects.get(id = i.pro.id)
            pro.stock += i.qty
            pro.save()
        cart_data.delete()
        return redirect('cart_view')
    else:
        return redirect('login')

def remove_from_cart(request, id):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email=request.session["login"])
        cart_data = Cart.objects.get(user=logged_in,id=id)
        pro = Product.objects.get(id=cart_data.pro.id)
        pro.stock += cart_data.qty
        pro.save()
        cart_data.delete()
        return redirect('cart_view')
    else:
        return redirect('login')
    
def orderhistory(request):
    if 'login' in request.session:
        logged_in = Registration.objects.get(email=request.session["login"])
        orders = Order.objects.filter(ordered=True , user__email = request.session['login']).order_by("-id")
        return render(request,'orderhistory.html',{'logged_in':True,'orders':orders})
    else:
        return redirect('login')
    
def single_invoice(request):
    if 'login' in request.session:
        id = request.GET['id']
        order = get_object_or_404(Order,id=id)
        param = {'order':order}
        return render(request,"invoice.html",param)
    else:
        return redirect('login')
    
    