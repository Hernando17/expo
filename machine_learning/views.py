from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category, Customer, Order
from django.contrib.auth.forms import AuthenticationForm
from .forms import ProductForm, CategoryForm, UserRegistry, CustomerForm, OrderForm
from django.db import transaction
import pickle
import os
import numpy as np
from django.http import HttpResponse
from sklearn.preprocessing import LabelEncoder

@login_required
def index(request):
    category_count = Category.objects.count()
    product_count = Product.objects.count()
    customer_count = Customer.objects.count()
    order_count = Order.objects.count()

    data = {
        'category_count': category_count,
        'product_count': product_count,
        'customer_count': customer_count,
        'order_count': order_count,
    }
    return render(request, 'index.html', data)

def register(request):
    if request.method == "POST":
        form = UserRegistry(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully. You can now log in.")
            return redirect("login")
    else:
        form = UserRegistry()
    context = {"register": "Register", "form": form}
    return render(request, "user/register.html", context)

def anonymous_required(function=None, redirect_url=None):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url if redirect_url else '/')
            else:
                return view_func(request, *args, **kwargs)
        return _view
    if function:
        return _decorator(function)
    return _decorator

@anonymous_required(redirect_url='/')
def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
            form = AuthenticationForm()
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def user(request):
    context = {"profile": "User Profile"}
    return render(request, "user/user.html", context)

@login_required
def category_index(request):
    hasil = Category.objects.all()
    data = {
        'data':hasil,
    }   
    return render(request, 'category/index.html', data)

@login_required
def category_create(request):
    submitted = False
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil dibuat')
            return redirect('/category/')
        else:
            error = form.errors
    else:
        form = CategoryForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'category/create.html', {'form' : form, 'submitted' : submitted})

@login_required
def category_edit(request, code):
    category = Category.objects.get(code=code)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diedit')
            return redirect('/category/')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'category/edit.html', {'form' : form})

@login_required
def category_detail(request, code):
    category = Category.objects.get(code=code)
    # products = Product.objects.get(code=code).product_set.all()
    products = Product.objects.filter(category=category)
    print(products, "productssssssssssss")
    return render(request, 'category/detail.html', {'category' : category, 'products' : products})

@login_required
def category_delete(request, code):
    dt = Category.objects.get(code=code)
    dt.delete()
    messages.success(request, 'Data berhasil dihapus')
    return redirect("/category/")

@login_required
def product_index(request):
    hasil = Product.objects.all()
    data = {
        'data':hasil,
    }   
    return render(request, 'product/index.html', data)

@login_required
def product_create(request):
    submitted = False
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil dibuat')
            return redirect('/product/')
        else:
            error = form.errors
    else:
        form = ProductForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'product/create.html', {'form' : form, 'submitted' : submitted})

@login_required
def product_edit(request, code):
    product = Product.objects.get(code=code)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diedit')
            return redirect('/product/')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'product/edit.html', {'form' : form})

@login_required
def product_delete(request, code):
    dt = Product.objects.get(code=code)
    dt.delete()
    messages.success(request, 'Data berhasil dihapus')
    return redirect("/product/")

@login_required
def customer_index(request):
    hasil = Customer.objects.all()
    data = {
        'data': hasil,
    }   
    return render(request, 'customer/index.html', data)

@login_required
def customer_create(request):
    submitted = False
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil dibuat')
            return redirect('/customer/')
        else:
            error = form.errors
    else:
        form = CustomerForm()
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'customer/create.html', {'form' : form, 'submitted' : submitted})

@login_required
def customer_edit(request, id):
    customer = Customer.objects.get(id=id)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data berhasil diedit')
            return redirect('/customer/')
    else:
        form = CustomerForm(instance=customer)
    
    return render(request, 'customer/edit.html', {'form' : form})

@login_required
def customer_delete(request, id):
    dt = Customer.objects.get(id=id)
    dt.delete()
    messages.success(request, 'Data berhasil dihapus')
    return redirect("/customer/")


# @login_required
# def warehouse_index(request):
#     hasil = Warehouse.objects.all()
#     data = {
#         'data': hasil,
#     }   
#     return render(request, 'warehouse/index.html', data)

# @login_required
# def warehouse_create(request):
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Warehouse created successfully.')
#             return redirect('/warehouse/')
#     else:
#         form = WarehouseForm()
#     return render(request, 'warehouse/create.html', {'form': form})

# @login_required
# def warehouse_edit(request, name):
#     warehouse = Warehouse.objects.get(name=name)
#     if request.method == 'POST':
#         form = WarehouseForm(request.POST, instance=warehouse)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Warehouse updated successfully.')
#             return redirect('/warehouse/')
#     else:
#         form = WarehouseForm(instance=warehouse)
#     return render(request, 'warehouse/edit.html', {'form': form})

# @login_required
# def warehouse_delete(request, id):
#     warehouse = Warehouse.objects.get(id=id)
#     warehouse.delete()
#     messages.success(request, 'Warehouse deleted successfully.')
#     return redirect("/warehouse/")

@login_required
def order_index(request):
    hasil = Order.objects.all()
    data = {
        'data': hasil,
    }   
    return render(request, 'order/index.html', data)

@login_required
def order_create(request):
    orders = Order.objects.all()
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                instance = form.save(commit=False)
                instance.created_by = request.user

                product = Product.objects.select_for_update().get(pk=instance.product.pk)
                if instance.quantity > product.quantity:
                    messages.error(request, 'Insufficient product quantity.')
                    return render(request, "order/create.html", {"title": "Orders", "orders": orders, "form": form})
                    
                product.quantity -= instance.quantity
                product.save()

                # Load the model and LabelEncoder
                model = load('satisfaction_model.joblib')
                label_enc = LabelEncoder()

                # Prepare the data for prediction
                customer_type = instance.customer.customer_type
                gender = instance.customer.gender
                product_category = instance.product.product_category
                unit_price = instance.product.unit_price
                quantity = instance.quantity
                payment_type = instance.payment_type
                total = instance.total()
                discount = instance.discount

                # Transform the input data using LabelEncoder
                customer_type = label_enc.fit_transform([customer_type])[0]
                gender = label_enc.fit_transform([gender])[0]
                product_category = label_enc.fit_transform([product_category])[0]
                payment_type = label_enc.fit_transform([payment_type])[0]

                # Make a prediction
                y_pred = model.predict([[customer_type, gender, product_category, unit_price, quantity, payment_type, total, discount]])

                prediction = round(y_pred[0], 3)
                instance.prediction = prediction

                # Categorize the prediction
                if prediction <= 3:
                    satisfaction = "Not Satisfied"
                elif 4 <= prediction <= 6:
                    satisfaction = "Quite Satisfied"
                elif 7 <= prediction <= 8:
                    satisfaction = "Satisfied"
                else:  # 9 <= prediction <= 10
                    satisfaction = "Very Satisfied"
        
                instance.satisfaction = satisfaction

                instance.save()

                return redirect("order_list")
    else:
        form = OrderForm()
    context = {"title": "Orders", "orders": orders, "form": form}
    return render(request, "order/create.html", context)

def make_prediction(instance):
    # Load the model and LabelEncoder
    model = load('satisfaction_model.joblib')
    label_enc = LabelEncoder()

    # Prepare the data for prediction
    customer_type = instance.customer.customer_type
    gender = instance.customer.gender
    product_category = instance.product.product_category
    unit_price = instance.product.unit_price
    quantity = instance.quantity
    payment_type = instance.payment_type
    total = instance.total()
    discount = instance.discount

    # Transform the input data using LabelEncoder
    customer_type = label_enc.fit_transform([customer_type])[0]
    gender = label_enc.fit_transform([gender])[0]
    product_category = label_enc.fit_transform([product_category])[0]
    payment_type = label_enc.fit_transform([payment_type])[0]

    # Make a prediction
    y_pred = model.predict([[customer_type, gender, product_category, unit_price, quantity, payment_type, total, discount]])


    prediction = round(y_pred[0], 3)
    instance.prediction = prediction

    # Categorize the prediction
    if prediction <= 3:
        satisfaction = "Not Satisfied"
    elif 4 <= prediction <= 6:
        satisfaction = "Quite Satisfied"
    elif 7 <= prediction <= 8:
        satisfaction = "Satisfied"
    else:  # 9 <= prediction <= 10
        satisfaction = "Very Satisfied"

    instance.satisfaction = satisfaction

    instance.save()

@login_required
def order_edit(request, order_id):
    with transaction.atomic():
        order = get_object_or_404(Order, pk=order_id)
        original_quantity = order.quantity  
        original_product = order.product 

        if request.method == "POST":
            form = OrderForm(request.POST, instance=order)
            if form.is_valid():
                updated_order = form.save(commit=False)
                updated_quantity = updated_order.quantity
                updated_product = updated_order.product  

                if original_product != updated_product:
                    original_product.quantity += original_quantity
                    original_product.save()

                product = Product.objects.select_for_update().get(pk=updated_product.pk)

                if updated_quantity > product.quantity + original_quantity:
                    messages.error(request, 'Insufficient product quantity.')
                    return redirect('edit', order_id=order_id)

                product.quantity = product.quantity - updated_quantity + (original_quantity if original_product == updated_product else 0)
                product.save()

                make_prediction(updated_order)

                updated_order.save()

                return redirect('order_list')
        else:
            form = OrderForm(instance=order)
    return render(request, 'order/edit.html', {'form': form})

@login_required
def order_delete(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    messages.success(request, 'order deleted successfully.')
    return redirect("/order/")

def test(request):
    return render(request, 'test.html')

from django.shortcuts import render

from joblib import load
model = load('satisfaction_model.joblib')

label_enc = LabelEncoder()

def predictor(request):
    if request.method == 'POST':
        customer_type = request.POST['customer_type']
        gender = request.POST['gender']
        product_category = request.POST['product_category']
        unit_price = float(request.POST['unit_price'])
        quantity = int(request.POST['quantity'])
        payment_type = request.POST['payment_type']
        total = float(request.POST['total'])
        discount = float(request.POST['discount'])

        # Transform the input data using LabelEncoder
        customer_type = label_enc.fit_transform([customer_type])[0]
        gender = label_enc.fit_transform([gender])[0]
        product_category = label_enc.fit_transform([product_category])[0]
        payment_type = label_enc.fit_transform([payment_type])[0]

        y_pred = model.predict([[customer_type, gender, product_category, unit_price, quantity, payment_type, total, discount]])

        return render(request, 'test.html', {'result' : y_pred})
    return render(request, 'test.html')
