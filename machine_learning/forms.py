from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import *

class UserRegistry(UserCreationForm):
    email = forms.EmailField()
    address = forms.CharField()
    mobile = forms.CharField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "address", "mobile", "password1", "password2"]

    def save(self, commit=True):
        user = super(UserRegistry, self).save(commit=False)
        if commit:
            user.save()
            user_profile = UserProfile(user=user, address=self.cleaned_data['address'], mobile=self.cleaned_data['mobile'])
            user_profile.save()
        return user

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['code', 'name', 'category', 'price', 'quantity']
        labels = {
            'code' : 'Kode Produk',
            'name' : 'Nama Produk',
            'price' : 'Harga Produk',
            'quantity' : 'Stok Produk',
            'category' : 'Kategori Produk',
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'price' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'quantity' : forms.NumberInput(attrs={'class' : 'form-control'}),
            'category' : forms.Select(attrs={'class' : 'form-control'}),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['code', 'name']
        labels = {
            'code' : 'Kode Kategori',
            'name' : 'Nama Kategori'
        }
        widgets = {
            'code' : forms.TextInput(attrs={'class' : 'form-control'}),
            'name' : forms.TextInput(attrs={'class' : 'form-control'})
        }

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'gender', 'email', 'mobile', 'address', 'customer_type']  
        labels = {
            'name' : 'Full Name',
            'gender' : 'Gender',
            'email' : 'email',
            'mobile' : 'Mobile',
            'address' : 'Address',
            'customer_type' : 'Customer Type', 
            
        }
        widgets = {
            'name' : forms.TextInput(attrs={'class' : 'form-control'}),
            'gender' : forms.Select(attrs={'class' : 'form-control'}),  
            'email' : forms.EmailInput(attrs={'class' : 'form-control'}),
            'mobile' : forms.TextInput(attrs={'class' : 'form-control'}),
            'address' : forms.TextInput(attrs={'class' : 'form-control'}),
            'customer_type' : forms.Select(attrs={'class' : 'form-control'}), 
        }

# class WarehouseForm(ModelForm):
#     class Meta:
#         model = Warehouse
#         fields = ['name', 'location', 'pic', 'mobile']
#         labels = {
#             'name' : 'Warehouse Name',
#             'location' : 'Warehouse Location',
#             'pic' : 'Person In Charge',
#             'mobile' : 'Mobile Number'
#         }
#         widgets = {
#             'name' : forms.TextInput(attrs={'class' : 'form-control'}),
#             'location' : forms.TextInput(attrs={'class' : 'form-control'}),
#             'pic' : forms.Select(attrs={'class' : 'form-control'}),
#             'mobile' : forms.TextInput(attrs={'class' : 'form-control'}),
#        }

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'quantity', 'customer', 'payment_type', 'discount']
        labels = {
            'product': 'Product',
            'quantity': 'Quantity',
            'customer': 'Customer',
            'payment_type': 'Payment Type',  
            'discount': 'Discount'  
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-control'}),  
            'discount': forms.Select(attrs={'class': 'form-control'}),  
        }

