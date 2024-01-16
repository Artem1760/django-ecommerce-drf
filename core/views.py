from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse

from book.models import Book, Category
from .forms import ContactUsForm
from .models import ContactInformation


def index(request):
    """View for the home page"""
    books = Book.objects.filter(is_active=True)[:8]
    categories = Category.objects.filter(is_active=True)[:6]
    context = {
        'books': books,
        'categories': categories,
        'title': 'Home | Molla'
    }
    return render(request, 'core/index.html', context)


def about_us_view(request):
    context = {'title': 'About Us'}
    return render(request, 'core/about_us.html', context)


def contact_view(request):
    """
    Handles the contact form submission and renders the contact page.
    """
    form = ContactUsForm()

    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            # If the form is valid, set the user field and save the form
            form.instance.user = request.user if request.user.is_authenticated else None
            form.save()
            messages.success(request,
                             'Your message has been sent successfully!')
            redirect(reverse('core:contact'))
        messages.error(request, 'Please correct the errors below.')

    elif request.user.is_authenticated:
        # If the user is authenticated, set initial values for the form fields
        initial_data = {
            'user': request.user,
            'name': request.user.username,
            'email': request.user.email,
            'phone': request.user.phone,
        }
        form = ContactUsForm(initial=initial_data)

    context = {
        'title': 'Contact Us',
        'form': form,
        'data': ContactInformation.objects.all()
    }
    return render(request, 'core/contact.html', context)


def error_404_view(request, exception):
    """Page not found 404 error"""
    return render(request, 'core/404.html', {'title': 'Page Not Found'},
                  status=404)
