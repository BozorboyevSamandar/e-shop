from django.urls import path
from basic import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category-product/<slug>/',
         views.category_product, name='category-product'),
    path('product-detail/<slug>/', views.product_detail, name='product-detail'),
]
