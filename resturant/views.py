from django.shortcuts import render, get_object_or_404, redirect
from datetime import date
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth import login, logout, authenticate
from django.core.mail import send_mail
from django.template.loader import render_to_string
import json
import datetime

from .models import *
from .forms import RegisterUserForm, ContactForm



def index(request):

    all_items = Item.objects.all()
    special_items_list = []

    for item in all_items:
        if item.on_special == True:
            special_items_list.append(item)

    return render(request, "resturant/index.html", {
        "on_special_items": special_items_list
    })
    
    

def menu(request):

    all_items = Item.objects.all()

    return render(request, "resturant/full-menu.html", {
        "full_menu": all_items
    })
    
    

def menu_item(request, slug):

    item = get_object_or_404(Item, slug=slug)

    return render(request, "resturant/menu-item-detail.html", {
        "name" : item.name,
        "price": item.price,
        "mini_description": item.mini_description,
        "full_description": item.full_description,
        "image_url": item.image_url,
        "gluten_free": item.gluten_free,
    })
    
    

def contactus(request):
    if request.method == "POST":
        
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            html = render_to_string('emails/contactform.html',{
                'name': name,
                'email': email,
                'message': message, 
            })
            
            send_mail('The contact form subject', 'This is the message', 'noreply@teds.com', ['teds@gmail.com'], html_message=html)
            messages.success(request, ("Message Sent!"))
            return redirect('/contactus')

    else:
        form = ContactForm()
        return render(request, "resturant/contactus.html", {"form":form})
    
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login Successful!"))
            return redirect('/home')
        else:
            messages.error(request, ("There was an error logging in, try again..."))	
            return redirect('/login')	
        
    else:
        return render(request, "registration/login.html", {})
    
    

def logout_user(request):
    logout(request)
    messages.success(request, ("You Were Logged Out!"))
    return redirect('/home')



def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, ("Registration Successful!"))
            return redirect('/home')
        
    else:
        form = RegisterUserForm()

    return render(request, 'registration/register_user.html', {'form':form,})



def updateItem(request):
    data = json.loads(request.body)
    
    print("data: " )
    print(data)
    
    itemId = data['itemId']
    action = data['action']
    
    print("Action: ", action)
    print("itemId: ", itemId)
    
    customer = request.user.customer
    item = Item.objects.get(id=itemId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, item=item)
    
    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
        
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
        
    orderItem.save()
    
    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse("Item was added", safe=False)

		
  
def cart(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items': items, 'order': order}
    return render(request, "resturant/cart.html", context) 
  
  
  
def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        
    context = {'items': items, 'order': order}
    return render(request, 'resturant/checkout.html', context)


def processOrder(request):
    print("Data: ", request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == order.get_cart_total:
            order.complete = True
            
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                suburb=data['shipping']['suburb'],
                city=data['shipping']['city'],
                postcode=data['shipping']['postcode'],
            )
        
    else:
        print("User is not logged in")
        
    return JsonResponse('Payment complete!', safe=False)