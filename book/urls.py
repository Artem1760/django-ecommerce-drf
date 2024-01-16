from django.urls import path

from . import views

app_name = 'book'

urlpatterns = [

    # Book
    path('books/', views.book_list_filter, name='book-list'),
    path('books/tag-list/', views.tag_list, name='tag-list'),
    path('books/author-list/', views.author_list, name='author-list'),
    path('books/hot-offers/', views.hot_offers, name='hot-offers'),
    path('books/<slug>/', views.book_detail, name='book-detail'),
    path('books/author/<slug>/', views.authors, name='authors'),
    path('books/related-books/<slug>/', views.related_books,
         name='related-books'),
    path('books/tag/<slug>/', views.tags, name='tags'),

    # Review  
    path('books/<slug>/add-review/', views.add_review, name='add-review'),
    path('books/<pk>/delete-review/', views.delete_review,
         name='delete-review'),
    path('books/<pk>/update-review/', views.update_review,
         name='update-review'),

    # Category  
    path('categories/', views.category_list, name='category-list'),
    path('categories/<slug:slug>/', views.category_book_list, name='category'),

    # Search
    path('search/', views.search_view, name='search'),
]
