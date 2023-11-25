#from urllib import request
#from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import render,redirect,reverse
from django.views import View
from . models import Cart, Customer, Product, Category, SubCategory
from . forms import CustomerProfileForm,CustomerRegistrationForm,Upload
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.
def home(request):
    return render(request , "app/home.html")

def about(request):
    return render(request , "app/about.html")

def contact(request):
    return render(request , "app/contact.html")


def upload(request):
    if request.method == 'POST':
        form = Upload(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']  
            title = form.cleaned_data['title']  
            selling_price = form.cleaned_data['selling_price']
            discounted_price = form.cleaned_data['discounted_price']  
            publisher = form.cleaned_data['publisher'] 
            description = form.cleaned_data['description']  
            category = form.cleaned_data['category']
            subcategory = form.cleaned_data['subcategory'] 
            product_image = form.cleaned_data['product_image']
            
            return render(request , "app/upload.html")
    else:
        form = Upload()
    return render(request, 'app/upload.html', {'form': form})
'''
def upload(request):
    return render(request , "app/upload.html")'''


def payment_gateway(request):
    return render(request , "app/payment.html")


class SubCategoryView(View):
    def get(self, request,val): 
        standard = SubCategory.objects.filter(category=val)
        return render(request, "app/subcategory.html", locals())
class CategoryView(View):
    def get(self, request,val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, "app/category.html", locals())
    

class CategoryTitle(View):
    def get(self, request, val):  # subject name as parameter; initial-name of the book
        # Retrieve SubCategory object based on id=val
        subcategory = SubCategory.objects.filter(id=val).first()
        subject_name = subcategory.name if subcategory else None
        print("subcategory:", subcategory)      
        # Retrieve Category object based on the name of the category of the subcategory
        standard = Category.objects.filter(name=subcategory.category).first()
        category = subcategory.category if subcategory else None
        category_name = category.name if category else None
        print("category:", category.id)
        # Retrieve Product objects based on subcategory=subcategory and category=category
        product = Product.objects.filter(subcategory=subcategory, category=category)
        print("products:", product)
        # Retrieve titles based on category of the first product (if any)
        #title = product.values('title') if product else None
        title = SubCategory.objects.filter(category=standard.id)

        return render(request, "app/category.html", locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request, "app/productdetail.html", locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration Successful!")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'app/customerregistration.html',locals())
    
    
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_vaild():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! profile Save Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'app/profil.html',locals()) 

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',locals()) 
    
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'app/updateAddress.html',locals()) 
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request,"Congratulations! Profile Updated successfully")
        else:
            messages.warning(request,"Invalid Input Data")    
        return redirect("address")
    
def add_to_cart(request): 
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

def show_cart(request):
    user=request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for c in cart:
        value = c.quantity * c.product.discounted_Price
        amount += value
    totalamount = amount 
    return render(request, 'app/addtocart.html',locals())

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        print("product id:", prod_id)
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        print("C: ",c)
        print("C quantity: ",c.quantity)
        newc = c.quantity
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for c in cart:
            value = c.quantity * c.product.discounted_Price
            amount += value
        totalamount = amount 
        data = {
            'quantity':newc,
            'amount':amount,
            'totalamount':totalamount
        }
        print("data", data)
        return JsonResponse(data)
    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        newc = c.quantity
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for c in cart:
            value = c.quantity * c.product.discounted_Price
            amount += value
        totalamount = amount 
        data = {
            'quantity':newc,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user=request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for c in cart:
            value = c.quantity * c.product.discounted_Price
            amount += value
        totalamount = amount 
        data = {
            'quantity':c.quantity,
            'totalamount':totalamount
        }
        return JsonResponse(data)