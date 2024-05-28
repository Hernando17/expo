from django.contrib import admin
from .models import Category, Product, Order, Event
from import_export.admin import ImportExportModelAdmin

class CategoryAdmin(ImportExportModelAdmin):
    model = Category
    list_display = ("code", "name")
    search_fields = ["name"]

class ProductAdmin(ImportExportModelAdmin):
    model = Product
    list_display = ("code", "name", "price", "quantity", "uom", "category")
    list_filter = ["category"]
    search_fields = ["name"]

class OrderAdmin(ImportExportModelAdmin):
    model = Order
    list_display = ("id", "date", "product", "quantity", "total_price")
    list_filter = ["date"]
    search_fields = ["product"]

class EventAdmin(ImportExportModelAdmin):
    model = Event
    list_display = ("id", "name", "date")
    search_fields = ["name"]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Event, EventAdmin)