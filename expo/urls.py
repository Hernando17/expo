"""
URL configuration for expo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from machine_learning import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path("user/register/", views.register, name="register"),
    path('login/', views.login_view, name='login'),
    path("user/", views.user, name="user"),
    path('logout/', views.logout_view, name='logout'),

    path('product/', views.product_index, name='product_list'),
    path('product/create', views.product_create, name='product_create'),
    path('product/edit/<str:code>', views.product_edit, name='product_edit'),
    path('product/delete/<str:code>',views.product_delete, name='product_delete'),

    path('category/', views.category_index, name='category_list'),
    path('category/create', views.category_create, name='category_create'),
    path('category/edit/<str:code>', views.category_edit, name='category_edit'),
    path('category/delete/<str:code>',views.category_delete, name='category_delete'),

    path('customer/', views.customer_index, name='customer_list'),
    path('customer/create', views.customer_create, name='customer_create'),
    path('customer/edit/<str:id>', views.customer_edit, name='customer_edit'),
    path('customer/delete/<str:id>',views.customer_delete, name='customer_delete'),

    # path('warehouse/', views.warehouse_index, name='warehouse_list'),
    # path('warehouse/create', views.warehouse_create, name='warehouse_create'),
    # path('warehouse/edit/<str:name>', views.warehouse_edit, name='warehouse_edit'),
    # path('warehouse/delete/<str:name>',views.warehouse_delete, name='warehouse_delete'),

    path('order/', views.order_index, name='order_list'),
    path('order/create', views.order_create, name='order_create'),
    path('order/edit/<str:order_id>', views.order_edit, name='order_edit'),
    path('order/delete/<str:order_id>',views.order_delete, name='order_delete'),
]
