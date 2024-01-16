from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('about-us/', views.about_us_view, name='about-us'),
    path('contact-us/', views.contact_view, name='contact'),
]
