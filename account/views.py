from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView, View

from book.models import Book
from checkout.models import Order, Address
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import CustomerUser, CustomerProfile
from .token import account_activation_token


################### User creation ###################
class RegistrationView(CreateView):
    """
    View for user registration, sending activation email, and confirmation page.
    """
    template_name = 'account/registration/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('account:dashboard')

    def form_valid(self, form):
        """
        Process the valid registration form, create an inactive user,
        send activation email, and render the confirmation page.
        """
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.set_password(form.cleaned_data['password1'])
        user.is_active = False
        user.save()

        # Create the activation email message using a template
        current_site = get_current_site(self.request)
        subject = 'Activate your Account'
        message = render_to_string(
            'account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        try:
            # Send activation email to the user
            user.email_user(subject=subject, message=message)
        except Exception as e:
            print(f'Email sending failed: {e}')
        return render(self.request,
                      'account/registration/register_email_confirm.html',
                      {'form': form})


class AccountActivateView(View):
    """
    View to activate a user account based on the provided activation token.
    """
    template_name = 'account/registration/activation_invalid.html'

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            # Decode the UID from base64 and get the user
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomerUser.objects.get(pk=uid)
        except(
                TypeError, ValueError, OverflowError,
                CustomerUser.DoesNotExist):
            # Handle invalid or non-existent user
            user = None
            messages.success(request, 'Your account was created successfully.')

        if user is not None and account_activation_token.check_token(user,
                                                                     token):
            # If the user and token are valid, activate the account
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('account:login')

        return render(request, self.template_name)


##################### Dashboard #####################
@login_required
def dashboard(request):
    """Main user profile view"""
    orders = Order.objects.filter(user_id=request.user.id)
    addresses = Address.objects.filter(user=request.user)
    user_form = UserEditForm(instance=request.user.profile)

    context = {
        'orders': orders,
        'user_form': user_form,
        'addresses': addresses,
        'title': f'Profile | {request.user}',
    }
    return render(request, 'account/profile/dashboard.html', context)


@login_required
def edit_account_details(request):
    """
    View to edit the account details of the currently logged-in user.
    """
    if request.method == 'POST':
        # Create a UserEditForm instance with the current user's profile data
        user_form = UserEditForm(instance=request.user.profile,
                                 data=request.POST, files=request.FILES)

        if user_form.is_valid():
            # Save the form if it is valid
            user_form.save()
            messages.success(request,
                             'Your account details were updated successfully.')
            return redirect('account:dashboard')

        # If form is not valid, return an error response
        return HttpResponse('Error: Please check the fields requirements.')


@login_required(login_url='core:login')
def delete_user(request):
    user = CustomerProfile.objects.get(username=request.user.username)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        logout(request)
        messages.success(request, 'Your account was deleted successfully.')
        return redirect('core:index')

    return render(request, 'account/profile/account_delete.html')


##################### Address #####################
@login_required
def view_address(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, 'account/profile/addresses.html',
                  {'addresses': addresses})


@login_required
def add_address(request):
    """
    View to add a new address for the currently logged-in user.
    """
    if request.method == 'POST':
        # Create an instance of UserAddressForm with the provided POST data
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            # Save the address form, associate it with the current user
            created_address = address_form.save(commit=False)
            created_address.user = request.user
            address_form.save()

            # If the new address is set as default, update other addresses to default=False
            if created_address.default:
                Address.objects.filter(user=request.user).exclude(
                    pk=created_address.pk).update(default=False)

            messages.success(request, 'Address has been added.')
            return redirect('account:dashboard')
        else:
            # If form is not valid, show a warning message
            messages.warning(request,
                             'All required fields have to be filled in been added.')
    else:
        # Create an empty address form for GET requests
        address_form = UserAddressForm()
    return render(request, 'account/profile/add_edit_address.html',
                  {'address_form': address_form,
                   'title': 'Add | Edit Address'})


@login_required
def edit_address(request, id):
    """
    View to edit an existing address for the currently logged-in user.
    """
    if request.method == 'POST':
        address = Address.objects.get(pk=id, user=request.user)
        # Create an instance of UserAddressForm with the provided POST data
        # and the existing address instance
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            # Save the updated address form and handle default address logic
            updated_address = address_form.save()
            # If the updated address is set as default, update other addresses
            # to default=False
            if updated_address.default:
                Address.objects.filter(user=request.user).exclude(
                    pk=updated_address.pk).update(default=False)

            messages.success(request, 'Address has been updated.')
            return redirect('account:dashboard')
        else:
            # If form is not valid, show a warning message
            messages.warning(request, 'Please, check the fields.')
            return redirect('account:dashboard')
    else:
        # Get the address instance for GET requests
        address = Address.objects.get(pk=id, user=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'account/profile/add_edit_address.html',
                  {'address_form': address_form})


@login_required
def delete_address(request, id):
    """Delete address"""
    address = Address.objects.filter(pk=id, user=request.user).delete()
    messages.warning(request, 'Address was deleted.')
    return redirect('account:dashboard')


@login_required
def set_default(request, id):
    """Set default address"""
    Address.objects.filter(user=request.user, default=True).update(
        default=False)
    Address.objects.filter(pk=id, user=request.user).update(default=True)
    messages.success(request, 'Default Address has been set.')

    return redirect('account:dashboard')


##################### Orders #####################
@login_required
def user_orders(request):
    orders = Order.objects.filter(user_id=request.user.id)
    return render(request, 'account/profile//user_orders.html',
                  {'orders': orders})


#################### Wishlist ####################    
@login_required
def wishlist(request):
    """Wishlist view"""
    books = Book.objects.filter(users_wishlist=request.user)
    return render(request, 'account/wishlist.html',
                  {'wishlist': books, 'title': 'Wishlist'})


@login_required
def add_to_wishlist(request, id):
    """
    View to add or remove a book to/from the user's wishlist.
    """
    book = get_object_or_404(Book, id=id)
    if book.users_wishlist.filter(id=request.user.id).exists():
        # If the book is already in the user's wishlist, remove it
        book.users_wishlist.remove(request.user)
        messages.warning(request,
                         f'"{book.title}" has been removed from your WishList')
    else:
        # If the book is not in the user's wishlist, add it
        book.users_wishlist.add(request.user)
        messages.success(request, f'"{book.title}" added to your WishList')
    # store information and get back to the previous page
    return HttpResponseRedirect(request.META["HTTP_REFERER"])
