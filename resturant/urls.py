from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="homepage"), #homepage
    path("home", views.index, name="homepage"), #homepage
    path("menu", views.menu, name="menu-page"), #show all menu items
    path("menu/<slug:slug>", views.menu_item, name="menu-item-detail-page"), #particular menu item #/menu/butterchicken
    path("cart/", views.cart, name="cart"),
    path("contactus/", views.contactus, name="contactus"),
    path("login/", views.login_user, name="login_user"),
    path("register_user/", views.register_user, name="register_user"),
    path("logout/", views.logout_user, name="logout"),
    path("update_item/", views.updateItem, name="update_item"),
    path('checkout/', views.checkout, name="checkout"),
    path("process_order/", views.processOrder, name="update_item")
]