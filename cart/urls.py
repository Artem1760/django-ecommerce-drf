from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_summary, name='cart-summary'),
    path('add/', views.add_to_cart, name='cart-add'),
    path('update-delete/', views.cart_update_delete,
         name='cart-update-delete'),
    path('delete/', views.cart_preview_delete, name='cart-preview-delete'),
]
