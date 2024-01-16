from django.contrib import admin

from .models import ContactUs, ContactInformation, WorkDays


class WorkDaysInline(admin.TabularInline):
    model = WorkDays


class ContactInformationAdmin(admin.ModelAdmin):
    inlines = [WorkDaysInline, ]


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_date']
    readonly_fields = ['created_date']


admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(ContactInformation, ContactInformationAdmin)
