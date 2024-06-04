from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from joblib import load

# Load the model
satisfaction_model = load('satisfaction_model.joblib')

# Create your models here.
CUSTOMER_TYPES = [
    ('Member', 'Member'),
    ('Regular', 'Regular'),
]

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
]

PAYMENT_TYPES = [
    ('Qris', 'Qris'),
    ('Cash', 'Cash'),
    ('Transfer', 'Transfer'),
    ('Card', 'Card'),
]
Discount_CHOICES = [
    ('0', '0'),
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('25', '25'),
    ('30', '30'),
    ('35', '35'),
    ('40', '40'),
    ('45', '45'),
    ('50', '50'),
    ('55', '55'),
    ('60', '60'),
    ('65', '65'),
    ('70', '70'),
    ('75', '75'),
    ('80', '80'),
    ('85', '85'),
    ('90', '90'),
    ('95', '95'),
    ('100', '100'),
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=14)
    picture = models.ImageField(default="avatar.jpeg", upload_to="Pictures")

    def __str__(self) -> str:
        return self.user.username
    
class Category(models.Model):
    code = models.CharField(primary_key=True, max_length=25)
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'category'

# class Warehouse(models.Model):
#     id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=100)
#     location = models.CharField(max_length=255)
#     pic = models.ForeignKey(User, on_delete=models.CASCADE)
#     mobile = models.CharField(max_length=15)
    
#     def __str__(self):
#         return self.name

#     class Meta:
#         db_table = 'warehouse'

class Product(models.Model):
    UOM_CHOICES = (
        ('pcs', 'PCS'),
        ('pack', 'PACK'),
        ('bottle', 'BTL'),
        ('carton', 'CARTON'),
        ('kg', 'KG'),
    )

    code = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    uom = models.CharField(max_length=10, choices=UOM_CHOICES)
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    # warehouse = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'product'
    
class Event(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    date = models.DateField()

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'event'

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    customer_type = models.CharField(max_length=25, choices=CUSTOMER_TYPES, default='Regular')
    gender = models.CharField(max_length=25, choices=GENDER_CHOICES, default='Male')

    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.CharField(max_length=10, choices=Discount_CHOICES, default='0')
    payment_type = models.CharField(max_length=25, choices=PAYMENT_TYPES, default='Cash')
    # warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    prediction = models.IntegerField(null=True, blank=True)
    satisfaction = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.product} ordered quantity {self.quantity}"
    
    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError("Order quantity cannot be more than product quantity")
        if self.quantity == 0:
            raise ValidationError("Order quantity cannot be zero")
        
    def total(self):
        return self.product.unit_price * self.quantity

    class Meta:
        db_table = 'order'

