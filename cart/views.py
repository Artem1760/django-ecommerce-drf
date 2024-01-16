from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from book.models import Book, BookLanguage, BookType
from checkout.models import DeliveryOptions
from .cart import Cart
from .forms import AddToCartForm


def cart_summary(request):
    cart = Cart(request)
    deliveries = DeliveryOptions.objects.all()
    context = {
        'cart': cart,
        'title': 'Cart Summary',
        'deliveries': deliveries,
    }
    return render(request, 'cart/cart.html', context)


def add_to_cart(request):
    """Add book to the Cart"""
    if request.method == 'POST':
        form = AddToCartForm(request.POST)

        if form.is_valid():
            # If you select values from the book-detail template
            book_id = form.cleaned_data['book_id']
            book_qty = form.cleaned_data['book_qty']
            book_language_id = form.cleaned_data['language_id']
            book_type_id = form.cleaned_data['book_type_id']

            book = get_object_or_404(Book, id=book_id)
            language = get_object_or_404(BookLanguage, id=book_language_id)
            book_type = get_object_or_404(BookType, id=book_type_id)
        else:
            # If it's default values for language, quantity, and book_type
            book_id = form.cleaned_data['book_id']

            book = get_object_or_404(Book, id=book_id)
            book_qty = 1
            language = book.languages.first()
            book_type = book.book_type.first()

        cart = Cart(request)
        cart.add(book=book, quantity=book_qty, language=language,
                 book_type=book_type)
        messages.success(request, f'"{book}" has been added to the cart.')

    return redirect(request.META.get('HTTP_REFERER'))


############# Cart update/delete #############
def cart_update(request):
    """Helper function handles updating the cart"""
    cart = Cart(request)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'update_cart':
            for key, value in request.POST.items():

                if key.startswith('bookqty_'):
                    book_id = int(key.split('_')[1])
                    cart.update_quantity(book_id, int(value))

                elif key.startswith('language_'):
                    book_id = int(key.split('_')[1])
                    cart.update_language(book_id, int(value))

                elif key.startswith('type_'):
                    book_id = int(key.split('_')[1])
                    cart.update_type(book_id, int(value))

            messages.success(request, 'Cart has been updated.')
    return redirect(reverse('cart:cart-summary'))


def cart_delete(request):
    """Helper function handles removing a specific item in the cart"""
    cart = Cart(request)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action.startswith('remove_item_'):
            book_id = int(action.split('_')[2])
            book_instance = get_object_or_404(Book, id=book_id)
            cart.delete(book=book_instance)
            messages.warning(request,
                             f'"{book_instance}" has been removed from the Cart.')

    return redirect(reverse('cart:cart-summary'))


def cart_update_delete(request):
    """Allows whether delete item or update cart"""
    action = request.POST.get('action')

    if action == 'update_cart':
        return cart_update(request)
    elif action.startswith('remove_item_'):
        return cart_delete(request)

    return redirect(reverse('cart:cart-summary'))


##########################
def cart_preview_delete(request):
    """Delete item from the cart icon related to the main template"""
    cart = Cart(request)

    if request.method == 'POST':
        book_id = request.POST.get('remove_cart_item')
        book_instance = get_object_or_404(Book, id=book_id)
        cart.delete(book=book_instance)
        messages.warning(request,
                         f'"{book_instance}" has been removed from the Cart.')
    return redirect(request.META.get('HTTP_REFERER'))
