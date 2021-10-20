from django.urls import path

from order import views

urlpatterns = [
    path('shop-cart/', views.shopcart, name='shopcart'),
    path('deletefromcart/<int:pk>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct/', views.orderproduct, name='orderproduct'),
    path('addshop-cart/<slug>/', views.addshopcart, name='add-shop-cart'),
]
