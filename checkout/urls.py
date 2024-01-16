from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('cart-update-delivery/', views.cart_update_delivery,
         name='cart-update-delivery'),
    path('payment-selection/', views.payment_selection,
         name='payment-selection'),
    path('payment-complete/', views.payment_complete, name='payment-complete'),
    path('payment-successful/', views.payment_successful,
         name='payment-successful'),
    path('payment-failed/', views.payment_failed, name='payment-failed'),
]
