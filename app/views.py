from django.db.models import Q
from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Customer, OrderPlaced
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
 def get(self,request):
  totalitem = 0
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  laptops = Product.objects.filter(category='L')
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'topwears':topwears,'totalitem': totalitem , 'bottomwears': bottomwears, 'mobiles': mobiles, 'laptops':laptops})


def searchview(request):
 if 'search' in request.GET:
  prod = request.GET('search')
  product= Product.objects.filter(title__icontains=prod)
 else:
  product = Product.objects.all()

 print(product, "=======???????????????")


 context= {
  'product': product,
 }


 return render(request,'app/base.html',context)


@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user==user]
  if cart_product:
   for p in cart_product:
    temp_amount = (p.quantity * p.product.discounted_price)
    amount+=temp_amount
    total_amount = amount + shipping_amount

   return render(request, 'app/addtocart.html', {'carts':cart, 'total_amount':total_amount, 'amount': amount})
  else:
   return render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'total_amount': amount + shipping_amount
  }
 return JsonResponse(data)

def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'total_amount': amount + shipping_amount
  }
 return JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount

  data = {
   'amount': amount,
   'total_amount': amount + shipping_amount
  }
 return JsonResponse(data)


class ProductDetailView(View):
 def get(self,request,pk):
  totalitem = 0
  product = Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
   totalitem = len(Cart.objects.filter(user=request.user))
   item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
   product = Product.objects.get(pk=pk)
  return render(request,'app/productdetail.html', {'product' : product, 'totalitem':totalitem, 'item_already_in_cart': item_already_in_cart})


@login_required
def add_to_cart(request):
 user=request.user
 product_id=request.GET.get('prod_id')
 product=Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

def buy_now(request):
 return render(request, 'app/buynow.html')

def about_us(request):
 return render(request, 'app/about_us.html')

def profile(request):
 return render(request, 'app/profile.html')

def address(request):
 adr=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'adr':adr, 'active':'btn-primary'})

@login_required
def orders(request):
 op= OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'order_placed':op})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(selling_price__lt=10000)
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(selling_price__gt=10000)
 return render(request, 'app/mobile.html', {'mobiles': mobiles})

def laptop(request,data=None):
 if data == None:
  laptops = Product.objects.filter(category='L')
 elif data == 'HP' or data == 'Dell':
  laptops = Product.objects.filter(category='L').filter(brand=data)
 elif data == 'below':
  laptops = Product.objects.filter(category='L').filter(selling_price__lt=10000)
 elif data == 'above':
  laptops = Product.objects.filter(category='L').filter(selling_price__gt=10000)
 return render(request, 'app/laptop.html', {'laptops': laptops})

def topwear(request,data=None):
 if data == None:
  topwears = Product.objects.filter(category='TW')
 elif data == 'Raymond' or data == 'Lee':
  topwears = Product.objects.filter(category='TW').filter(brand=data)
 elif data == 'below':
  topwears = Product.objects.filter(category='TW').filter(selling_price__lt=500)
 elif data == 'above':
  topwears = Product.objects.filter(category='TW').filter(selling_price__gt=500)
 return render(request, 'app/topwear.html', {'topwears': topwears})

def bottomwear(request,data=None):
 if data == None:
  bottomwears = Product.objects.filter(category='BW')
 elif data == 'Raymond' or data == 'Lee':
  bottomwears = Product.objects.filter(category='BW').filter(brand=data)
 elif data == 'below':
  bottomwears = Product.objects.filter(category='BW').filter(selling_price__lt=500)
 elif data == 'above':
  bottomwears = Product.objects.filter(category='BW').filter(selling_price__gt=500)
 return render(request, 'app/bottomwear.html', {'bottomwears': bottomwears})




class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request, 'app/customerregistration.html', {'form':form})

 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request,'Congratulations! You have registered successfully')
   form.save()
  return render(request, 'app/customerregistration.html', {'form': form})

@login_required
def checkout(request):
 user =  request.user
 adr = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)
 amount = 0.0
 shipping_amount = 70.0
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == user]
 if cart_product:
  for p in cart_product:
   temp_amount = (p.quantity * p.product.discounted_price)
   amount += temp_amount
  total_amount = amount + shipping_amount

 return render(request, 'app/checkout.html', {'adr':adr,'cart_items':cart_items, 'total_amount': total_amount})

@login_required
def payment_done(request):
 if request.method == 'GET':
  user=request.user
  custid = request.GET.get('custid')
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)

  for c in cart:
   OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
   c.delete()
  return redirect("orders")


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
 def get(self,request):
  form=CustomerProfileForm()
  return  render(request,'app/profile.html',{'form':form, 'active':'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   user = request.user
   name=form.cleaned_data['name']
   phone=form.cleaned_data['phone']
   locality=form.cleaned_data['locality']
   city=form.cleaned_data['city']
   zipcode=form.cleaned_data['zipcode']
   state=form.cleaned_data['state']

   reg = Customer(user=user, name=name, phone=phone, locality=locality, city=city, zipcode=zipcode, state=state)
   reg.save()
   messages.success(request,'Congratulations! Your Profile is updated Successfully')

  return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary'})