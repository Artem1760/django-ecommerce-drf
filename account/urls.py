from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    # Log in/out    
    path('login/',
         auth_views.LoginView.as_view(template_name='account/login.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Register
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('activate/<slug:uidb64>/<slug:token>/',
         views.AccountActivateView.as_view(), name='activate'),

    # Reset password    
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset/password_reset_form.html',
        email_template_name='account/password_reset/password_reset_email.html'),
         name='password-reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset/password_reset_done.html'),
         name='password-reset-done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset/password_reset_confirm.html'),
         name='password-reset-confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset/password_reset_complete.html'),
         name='password-reset-complete'),

    # User dashboard 
    path('profile/', views.dashboard, name='dashboard'),
    path('profile/account-details/', views.edit_account_details,
         name='account-details'),
    path('profile/delete-user/', views.delete_user, name='delete-user'),

    # Address
    path('addresses/', views.view_address, name='addresses'),
    path('address/add/', views.add_address, name='add-address'),
    path('addresses/edit/<slug:id>/', views.edit_address, name='edit-address'),
    path('addresses/delete/<slug:id>/', views.delete_address,
         name='delete-address'),
    path('addresses/set-default/<slug:id>/', views.set_default,
         name='set-default'),

    # Order
    path('orders/', views.user_orders, name='user-orders'),

    # Wish List
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/add-to-wishlist/<int:id>/', views.add_to_wishlist,
         name='user-wishlist'),
]
