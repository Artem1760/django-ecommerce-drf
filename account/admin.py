from django.contrib import admin

from .models import CustomerUser, CustomerProfile


class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone']
    list_editable = ['phone']


class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'phone']
    list_editable = ['phone']


admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(CustomerProfile, CustomerProfileAdmin)
