from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    #rating = models.IntegerField( validators=[MinValueValidator(1), MaxValueValidator(5)])
    mini_description = models.CharField(max_length=200)
    full_description = models.CharField(max_length=500)
    image_url = models.CharField(max_length=500)
    gluten_free = models.BooleanField(default=False)
    on_special = models.BooleanField(default=False)
    slug = models.SlugField(default="", blank=True, null=False, db_index=True) # Harry Potter 1 -> harry-potter-1 -> search engine optimization
    #db_index is useful for when you use a keyword to search the database
    #readonly_fields = ("slug",)


    def get_absolute_url(self):
        #return reverse("book-detail", args=[self.id])
        return reverse("book-detail", args=[self.slug])
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.price})"
    
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.name)
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return str(self.id)
    
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    @property 
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
    
class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.item.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    suburb = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    postcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.address)
    




