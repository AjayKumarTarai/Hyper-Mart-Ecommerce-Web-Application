from django.shortcuts import render, redirect
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobile = Product.objects.filter(category='M')
  laptop = Product.objects.filter(category='L')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'mobile':mobile, 'laptop':laptop, 'totalitem':totalitem})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')
class ProductDetailView(View):
 def get(self, request, pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart =False
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    item_already_in_cart =Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request, 'app/productdetail.html',{'product':product, 'item_already_in_cart':item_already_in_cart, 'totalitem':totalitem})

@login_required 
def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required 
def show_cart(request):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
    user = request.user
    cart = Cart.objects.filter(user=user)
    print(cart)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
   # print(cart_product)
    if cart_product:
      for p in cart_product:
        tempamount = (p.quantity * p.product.discounted_price)
        amount += tempamount
        totalamount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'carts':cart, 'shipping':shipping_amount, 'totalamount':totalamount, 'amount':amount, 'totalitem':totalitem})
    else:
      return render(request, 'app/emptycart.html', {'totalitem':totalitem})
  
def plus_cart(request):
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:  
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data = {
       'quantity': c.quantity,
       'amount': amount,
       'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)


def minus_cart(request):
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data = {
       'quantity': c.quantity,
       'amount': amount,
       'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)

@login_required          
def remove_cart(request):
 if request.method == 'GET':
    prod_id = request.GET['prod_id']
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    data = {
       'amount': amount,
       'totalamount':amount + shipping_amount
      }
    return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required 
def address(request):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 add = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required 
def orders(request):
 op = OrderPlaced.objects.filter(user = request.user)
 return render(request, 'app/orders.html',{'order_placed':op})

# mobile items
def mobile(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data =='Redmi' or data =='Samsung' or data =='Oppo' or data=='Vivo' or data=='Realme':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data =='bellow':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__lt= 50000)
 elif data =='above':
   mobiles = Product.objects.filter(category='M').filter(discounted_price__gt= 50000)
 return render(request, 'app/mobile.html',{'mobiles':mobiles, 'totalitem':totalitem})


# Laptop items
def laptop(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
  Laptop = Product.objects.filter(category='L')
 elif data =='Hp' or data =='Dell' or data =='Assus' or data=='Accer' or data=='Apple':
  Laptop = Product.objects.filter(category='L').filter(brand=data)
 elif data =='bellow':
   Laptop = Product.objects.filter(category='L').filter(discounted_price__lt= 100000)
 elif data =='above':
   Laptop = Product.objects.filter(category='L').filter(discounted_price__gt= 100000)
 return render(request, 'app/laptop.html',{'Laptop':Laptop, 'totalitem':totalitem})

# topwears
def topwears(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data==None:
   topwear=Product.objects.filter(category="TW")
 elif data == 'Killer' or data == 'Uspolo' or data== 'RodStar' or data== 'Gean':
   topwear=Product.objects.filter(category='TW').filter(brand=data)
 elif data=='bellow':
   topwear=Product.objects.filter(category='TW').filter(discounted_price__lt=200)
 elif data=='above':
   topwear=Product.objects.filter(category='TW').filter(discounted_price__gt=200)
 return render(request, 'app/topwears.html', {'topwear': topwear, 'totalitem':totalitem}) 
   

# Bottomwear
def bottomwears(request, data=None):
 totalitem = 0
 if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
 if data == None:
  bottomwear = Product.objects.filter(category='BW')
 elif data =='Killer' or data =='Lee' or data =='RodStar' or data=='SPARKY':
  bottomwear = Product.objects.filter(category='BW').filter(brand=data)
 elif data =='bellow':
   bottomwear = Product.objects.filter(category='BW').filter(discounted_price__lt= 1000)
 elif data =='above':
   bottomwear = Product.objects.filter(category='BW').filter(discounted_price__gt= 1000)
 return render(request, 'app/bottomwears.html',{'bottomwear':bottomwear, 'totalitem':totalitem})

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html', {'form': form})
  
 def post(sels, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html', {'form': form})

@login_required 
def checkout(request):
  totalitem = 0
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  user =request.user
  add= Customer.objects.filter(user=user)
  cart_items= Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount =70.0
  totalamount=0.0
  cart_product = [p for p in Cart.objects.all() if p.user==request.user]
  if cart_product:
    for p in cart_product:  
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount
  return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_product, 'totalitem':totalitem})

@login_required 
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders") 


@method_decorator (login_required, name='dispatch')
class ProfileView(View):
 def get(self, request):
  totalitem = 0
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  form =  CustomerProfileForm()
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
 
 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   usr = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   reg.save()
   messages.success(request, 'Congratulation !! Profile Updated Successfully')
  return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'}) 