from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from .models import Product,Customer,Cart,OrderPlaced,Payment,Wishlist
from django.db.models import Q
import vnpay
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomerRegistrationForm,CustomerProfileForm
# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
       
    return render(request, 'app/home.html',locals())
@login_required
def about(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'app/about.html')
@login_required
def contact(request):
    totalitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/contact.html')
@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request,val):
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'app/category.html', locals())
@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request,val):
        product = Product.objects.filter(title=val)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        title = Product.objects.filter(category=product[0].category).values('title')
        return render(request, 'app/category.html', locals())
@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):

        product = Product.objects.get(pk=pk)
        wishitem=0
        totalitem = 0
        wishlist=None
        if request.user.is_authenticated:
            wishlist= Wishlist.objects.filter(Q(product=product) &Q(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
       
        return render(request, 'app/customerregistration.html',locals())
    
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulation !! Registered Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/customerregistration.html',locals())
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem=len(Wishlist.objects.filter(user=request.user))
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            reg = Customer(user=user,name=name,mobile=mobile,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congratulation !! Profile Updated Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/profile.html',locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
       
    return render(request, 'app/address.html',locals())
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        totalitem = 0
        wishitem=0
        if request.user.is_authenticated:
            wishitem = len(Wishlist.objects.filter(user=request.user))
            totalitem = len(Cart.objects.filter(user=request.user))
       
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals())
    def post(self,request,pk):
        customer = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(request.POST,instance=customer)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.zipcode = form.cleaned_data['zipcode']
            add.state = form.cleaned_data['state']
            add.save()
            messages.success(request, 'Congratulation !! Address Updated Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return redirect('address')
@login_required
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount=0.0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount+=value 
    totalamount=amount +40
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
       
    return render(request, 'app/addtocart.html',locals())
@method_decorator(csrf_exempt, name='dispatch')  # Disable CSRF protection for IPN endpoint
class PaymentIPN(View):
    def post(self, request):
        # Handle IPN (Instant Payment Notification) from VNPay
        # Process payment result and update your database accordingly
        # Return appropriate response to VNPay (e.g., HTTP 200 OK)
        pass

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        # Create billing and obtain payment URL from VNPay
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0.0
        # Convert total amount to VNPay format (example: 100000 VND)
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount+=value  
        totalamount = famount + 40
        vnpay_amount = int(totalamount * 100)  # Convert to VNPay amount format (VND)
        # client = vnpay.Client(
        #     api_key=settings.VNPAY_API_KEY,
        #     secret_key=settings.VNPAY_SECRET_KEY,
        #     endpoint=settings.VNPAY_ENDPOINT,
        # )
        # Construct data for VNPay API
        data = {
            "amount": vnpay_amount,
            "currency": "VND",
            "receipt": "order_receipt_id"  # Replace with actual order receipt ID
        }
        return render(request, 'app/checkout.html', locals())
        # Call VNPay API to create billing and get payment URL
        #try:
            #payment_response = client.create_payment(data)
            #vnp_payment_url = payment_response['data']['redirect_url']
            #return JsonResponse({'payment_url': vnp_payment_url})
        #except vnpay.VNPayException as e:
            #return JsonResponse({'error': str(e)})
@login_required
def payment_done(request):
    order_id= request.GET.get('order_id')
    payment_id= request.GET.get('payment_id')
    cust_id= request.GET.get('cust_id')
    print(cust_id)
    user=request.user
    customer = Customer.objects.get(id=cust_id)
    #to update payment status and payment id
    payment=Payment.object.get(vnpay_order_id=order_id)
    payment.paid=True
    payment.vnpay_payment_id = payment_id
    payment.save()
    #to save order details
    cart = Cart.objects.filter(user=user)
    for c in cart: 
        OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect('orders')

@login_required
def orders(request):
    totalitem = 0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',locals())


def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if 'prod_id' is missing
        user = request.user
        carts = Cart.objects.filter(product=prod_id, user=user)  # Filter carts for the specific product and user
        if carts.exists():  # Check if any carts exist for the given criteria
            cart = carts.first()  # Get the first cart object
            cart.quantity += 1
            cart.save()
            cart_items = Cart.objects.filter(user=user)  # Retrieve all cart items for the user
            amount = sum(p.quantity * p.product.discounted_price for p in cart_items)  # Calculate total amount
            totalamount = amount + 40
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            # Handle case where no cart exists for the given criteria
            return JsonResponse({'error': 'Cart item not found'}, status=404)
def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if 'prod_id' is missing
        user = request.user
        carts = Cart.objects.filter(product=prod_id, user=user)  # Filter carts for the specific product and user
        if carts.exists():  # Check if any carts exist for the given criteria
            cart = carts.first()  # Get the first cart object
            cart.quantity -= 1
            cart.save()
            cart_items = Cart.objects.filter(user=user)  # Retrieve all cart items for the user
            amount = sum(p.quantity * p.product.discounted_price for p in cart_items)  # Calculate total amount
            totalamount = amount + 40
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            # Handle case where no cart exists for the given criteria
            return JsonResponse({'error': 'Cart item not found'}, status=404)

def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')  # Use get() to avoid KeyError if 'prod_id' is missing
        user = request.user
        carts = Cart.objects.filter(product=prod_id, user=user)  # Filter carts for the specific product and user
        carts.delete()
        cart_items = Cart.objects.filter(user=user)  # Retrieve all cart items for the user
        if cart_items.exists():  # Check if any carts exist for the given criteria
            cart = cart_items.first()
            amount = sum(p.quantity * p.product.discounted_price for p in cart_items)  # Calculate total amount
            totalamount = amount + 40
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            # Handle case where no cart exists for the given criteria
            return JsonResponse({'error': 'Cart item not found'}, status=404)

def plus_wishlist(request):
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        Wishlist(user=request.user,product=product).save()
        data={
            'message':'Added to wishlist'
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method =="GET":
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        Wishlist.objects.filter(user=request.user,product=product).delete()
        data={
            'message':'Removed from wishlist'
        }
        return JsonResponse(data)
@login_required
def search(request):
    query = request.GET['search']
    totalitem=0
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(title__icontains=query)
    return render(request, 'app/search.html',locals())


# def plus_cart(request):
#     if request.method == "GET":
#         prod_id = request.GET['prod_id']
#         c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity+=1
#         c.save()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount+=value
#         totalamount = amount + 40
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount': totalamount
#         }
#         return JsonResponse(data)
         