import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from book.models import Book, BookLanguage, BookType

CustomerUser = settings.AUTH_USER_MODEL

STATUS_CHOICE = [
    ('pending', _('Pending')),
    ('out_for_delivery', _('Out for Delivery')),
    ('delivered', _('Delivered')),
    ('refund', _('Refund')),
    ('canceled', _('Canceled')),
]

PAYMENT_OPTION = [
    ('on_receive', _('On Receive')),
    ('paypal', _('PayPal')),
]


class DeliveryOptions(models.Model):
    """
    The Delivery methods table continuing all delivery
    """
    delivery_name = models.CharField(max_length=100)
    delivery_price = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Delivery Option')
        verbose_name_plural = _('Delivery Options')
        ordering = ('delivery_price',)

    def __str__(self):
        return self.delivery_name


class Order(models.Model):
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE,
                             related_name='order_user')
    oid = ShortUUIDField(verbose_name=_('Order ID'), unique=True, length=10,
                         prefix='oid')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery = models.ForeignKey('DeliveryOptions', on_delete=models.SET_NULL,
                                 null=True, verbose_name='delivery_options')
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    payment_option = models.CharField(max_length=255, choices=PAYMENT_OPTION,
                                      default='on_receive')
    billing_status = models.BooleanField(default=False, null=True)
    order_status = models.CharField(verbose_name=_('Order status'),
                                    choices=STATUS_CHOICE, max_length=50,
                                    default='pending')
    created_date = models.DateTimeField(auto_now_add=True)
    shipping_address = models.ForeignKey('Address', on_delete=models.SET_NULL,
                                         null=True, related_name='addresses')

    class Meta:
        ordering = ('-created_date',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.oid} by {self.user.username}'

    def get_total_cost(self):
        """
        Get the total order price including the delivery cost.
        """
        return sum(item.get_cost() for item in self.items.all())

    def formatted_shipping_address(self):
        """
        Return a formatted string representing the shipping address.
        """
        if self.shipping_address:
            return f'{self.shipping_address.first_name} {self.shipping_address.last_name}, ' \
                   f'{self.shipping_address.street_address}, {self.shipping_address.town_city}, ' \
                   f'{self.shipping_address.country}'
        return 'N/A'

    formatted_shipping_address.short_description = 'Shipping Address'


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE,
                              related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_price = models.DecimalField(max_digits=10, decimal_places=2)
    language = models.ForeignKey(BookLanguage, on_delete=models.SET_NULL,
                                 null=True)
    book_type = models.ForeignKey(BookType, on_delete=models.SET_NULL,
                                  null=True)

    class Meta:
        verbose_name = _('Order item')
        verbose_name_plural = _('Order items')

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'Order item: {self.id}'


class Address(models.Model):
    """
    Address for delivery
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomerUser, verbose_name=_('Customer'),
                             on_delete=models.CASCADE,
                             related_name='addresses')
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    postcode = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    town_city = models.CharField(max_length=150)
    country_state = models.CharField(_('State'), max_length=150)
    delivery_instructions = models.CharField(max_length=255, null=True,
                                             blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    default = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f'{self.id}'

    def get_absolute_url(self):
        return reverse('account:set-default', kwargs={'slug': self.id})
