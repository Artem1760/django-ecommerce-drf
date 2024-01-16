from django import forms
from django.contrib import admin

from .models import DeliveryOptions, Order, OrderItem, Address


class OrderItemAdminForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'book', 'quantity', 'price', 'subtotal_price',
                  'language', 'book_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter language and book_type choices based on the selected book
        book_instance = self.instance.book if self.instance and hasattr(
            self.instance, 'book') else None

        if book_instance:
            self.fields['language'].queryset = book_instance.languages.all()
            self.fields['book_type'].queryset = book_instance.book_type.all()


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    form = OrderItemAdminForm
    list_display = ['order', 'book', 'quantity', 'price', 'subtotal_price',
                    'language', 'book_type']


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ['oid', 'order_status', 'payment_option', 'billing_status',
                    'formatted_shipping_address']
    list_display_links = ['oid']
    list_editable = ['order_status']


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Address)
admin.site.register(DeliveryOptions)
