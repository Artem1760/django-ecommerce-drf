from django.urls import path

from .search.views import SearchListView
from . import views

app_name = 'api'

urlpatterns = [
    # User   
    path('v1/users/', views.UserListCreateApiView.as_view(),
         name='user-list-create'),
    path('v1/user/<int:pk>/', views.UserGetUpdateDestroyAPIView.as_view(),
         name='user'),

    # Book
    path('v1/books/', views.BookListCreateApiView.as_view(),
         name='book-list-create'),
    path('v1/book/<int:pk>/', views.BookGetUpdateDestroyAPIView.as_view(),
         name='book'),

    # BookLanguage 
    path('v1/books/languages/', views.LanguageListCreateApiView.as_view(),
         name='language-list-create'),
    path('v1/books/language/<int:pk>/',
         views.LanguageGetUpdateDestroyAPIView.as_view(), name='language'),

    # BookType
    path('v1/books/types/', views.BookTypeListApiView.as_view(),
         name='type-list-create'),
    path('v1/books/type/<int:pk>/',
         views.BookTypeGetUpdateDestroyAPIView.as_view(), name='book-type'),

    # Category
    path('v1/books/categories/', views.CategoryListCreateApiView.as_view(),
         name='category-list-create'),
    path('v1/books/category/<int:pk>/',
         views.CategoryGetUpdateDestroyAPIView.as_view(), name='category'),

    # Publisher
    path('v1/books/publishers/', views.PublisherListCreateApiView.as_view(),
         name='publisher-list-create'),
    path('v1/books/publisher/<int:pk>/',
         views.PublisherGetUpdateDestroyAPIView.as_view(), name='publisher'),

    # Author
    path('v1/books/authors/', views.AuthorListCreateApiView.as_view(),
         name='author-list-create'),
    path('v1/books/author/<int:pk>/',
         views.AuthorGetUpdateDestroyAPIView.as_view(), name='author'),

    # BookReview
    path('v1/books/reviews/', views.ReviewListCreateApiView.as_view(),
         name='review-list-create'),
    path('v1/books/review/<int:pk>/', views.ReviewGetApiView.as_view(),
         name='review-detail'),
    path('v1/books/review/<int:pk>/update/',
         views.ReviewUpdateApiView.as_view(), name='review-update'),
    path('v1/books/review/<int:pk>/delete/',
         views.ReviewDeleteApiView.as_view(), name='review-delete'),

    # Order
    path('v1/orders/', views.OrderListApiView.as_view(), name='order-list'),
    path('v1/order/<int:pk>/', views.OrderGetDestroyAPIView.as_view(),
         name='order'),

    # Search
    path('v1/search/', SearchListView.as_view(), name='search')
]
