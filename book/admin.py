from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    Category,
    Book,
    BookImage,
    BookLanguage,
    BookReview,
    BookType,
    Author,
    Publisher,
    FilterPrice
)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ['name']}


class BookImageInline(admin.TabularInline):
    model = BookImage


class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageInline, ]
    list_display = ['title', 'category', 'is_active', 'get_html_image']
    list_editable = ['category', 'is_active']
    prepopulated_fields = {'slug': ['title']}
    list_display_links = ('title',)

    def get_html_image(self, object):
        if object.cover:
            return mark_safe(f"<img src='{object.cover.url}' width=50>")

    get_html_image.short_description = 'Cover'


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {'slug': ['name']}


class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_display_links = ('name',)
    search_fields = ('name',)


class BookLanguageAdmin(admin.ModelAdmin):
    list_display = ('id', 'language')
    list_display_links = ('language',)
    search_fields = ('language',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookType)
admin.site.register(BookLanguage, BookLanguageAdmin)
admin.site.register(BookReview)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(FilterPrice)

admin.site.site_title = 'Admin dashboard'
admin.site.site_header = 'Admin dashboard for Molla'
