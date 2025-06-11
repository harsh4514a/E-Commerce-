from django.shortcuts import *
from .models import *
from app1.models import Cart,Category,Product,Order
# Create your views here.
def SRegister(request):
    if request.method =='POST':
        store_reg = SellerRegistration()
        store_reg.name = request.POST['name']
        store_reg.email = request.POST['email']
        store_reg.add = request.POST['add']
        store_reg.mob = request.POST['mob']
        store_reg.password = request.POST['password']
        store_reg.c_password = request.POST['c_password']
        
        password = request.POST['password']
        c_password = request.POST['c_password']
        if password !=c_password:
            return render(request,'sregister.html',{'diff':"Enter confirm password same as password"})
                
        try:
            already_registered = SellerRegistration.objects.get(email = request.POST['email'])
            if already_registered:
                return render(request,'sregister.html',{'already_registered':"This email already registered"})
            
     
        except:
            store_reg.save()
            return render(request,'sregister.html',{'stored':"Registration succefull"})
       
            
                
        
    else:
        return render(request,'sregister.html')

def SLogin(request):
    if request.method == 'POST':
        try:
            register_data = SellerRegistration.objects.get(email = request.POST['email'])
            if request.POST['password'] == register_data.password:
                if register_data.accept:
                    request.session["Slogin"] = register_data.email
                    request.session["seller"] = True
                    return redirect('Sindex')
                else:
                    return render(request,'slogin.html',{'not_accept':"Your request is not accepted"})
            else:
                return render(request,'slogin.html',{'incorrect_Pass':"Please enter valid password .."})   
        except :          
            return render(request,'slogin.html',{'incorrect_email':"Please enter valid email.."})   

    
    return render(request,'slogin.html')   

def Slogout(request):
    del request.session['Slogin']  
    del request.session["seller"]     
    return redirect("Sindex")  


def Sindex(request):
    cat_data = Category.objects.all()
    
    if 'Slogin' in request.session:
        return render(request,"sindex.html",{'category':cat_data,'logged_in':True})

    else:
        return redirect("SLogin")
 
    

def Scatpro(request,id):
    if 'Slogin' in request.session and request.session['seller']:
        email = request.session['Slogin']
        seller = SellerRegistration.objects.get(email=email)
        category = Category.objects.get(id=id)        
        prod = Product.objects.filter(category = id,added_by=seller)
        return render(request,"scatpro.html",{'prod':prod,'logged_in':True, 'category_name': category.name})
        
    else:
        return redirect("SLogin")
        

def orders(request):
    if 'Slogin' in request.session and request.session['seller']:
        email = request.session['Slogin']
        seller = SellerRegistration.objects.get(email=email)
        my_orders = Cart.objects.filter(pro__added_by = seller,ordered=True).order_by("-id")
        param = {
            'my_orders':my_orders,
            'logged_in':True
        }
        return render(request,"sorders.html",param)
    
    else:
        return redirect("SLogin")
    
def add_product(request,id):
    if 'Slogin' in request.session and request.session['seller']:
        email = request.session['Slogin']
        seller = SellerRegistration.objects.get(email=email)
        name = request.POST["name"]
        price = request.POST["price"]
        stock = request.POST["stock"]
        image = request.FILE["image"]
        
        create_pro = Product.objects.create(
            category = id,
            added_by = seller,
            name=name,
            price= price,
            stock=stock,
            image=image,
        )
        create_pro.save()
        return HttpResponseRedirect("<script>alert('Product added successfully');windows.location.href='/seller/")
        return render(request,"add_product.html",{'logged_in':True})
    else:
        return redirect("SLogin")
        
        