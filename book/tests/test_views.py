from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import Category, Book, Author, FilterPrice, BookReview


class BookViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.filter_price = FilterPrice.objects.create(price='Test Price')
        self.book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            publication_date='2022-01-01',
            isbn='1234567890123',
            regular_price=10.00,
            discount_price=8.00,
            is_sale=True,
            description='Test Description',
            quantity=20,
            category=self.category,
            author=self.author,
            filter_price=self.filter_price,
        )

        self.user = get_user_model().objects.create_user(username='testuser',
                                                         email='test@user.com',
                                                         password='testpassword')
        self.review = BookReview.objects.create(book=self.book, user=self.user,
                                                star_rating=4,
                                                review='Test Review')

    def test_book_list_filter_view(self):
        response = self.client.get(reverse('book:book-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/product_list_filter.html')

    def test_book_detail_view(self):
        response = self.client.get(
            reverse('book:book-detail', kwargs={'slug': self.book.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/product_detail.html')

    def test_category_list_view(self):
        response = self.client.get(reverse('book:category-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/category_list.html')

    def test_category_book_list_view(self):
        response = self.client.get(
            reverse('book:category', kwargs={'slug': self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/generic_product_list.html')

    def test_related_books_view(self):
        response = self.client.get(
            reverse('book:related-books', kwargs={'slug': self.book.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/generic_product_list.html')

        # Check if the context contains the necessary keys
        self.assertIn('book', response.context)
        self.assertIn('books', response.context)
        self.assertIn('total_books_count', response.context)
        self.assertIn('related_books', response.context)
        self.assertIn('title', response.context)
        self.assertIn('obj', response.context)
        self.assertIn('is_paginated', response.context)

        # Check if the context values are as expected
        self.assertEqual(response.context['book'], self.book)

    def test_add_review_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(
            reverse('book:add-review', kwargs={'slug': self.book.slug}))
        self.assertEqual(response.status_code, 302)

        # Test adding a review
        response = self.client.post(
            reverse('book:add-review', kwargs={'slug': self.book.slug}),
            {'star_rating': 5, 'review': 'Great book'})
        self.assertEqual(response.status_code,
                         302)  # Redirect after a successful POST request
        self.assertEqual(BookReview.objects.count(),
                         1)  # Check if a new review is added

    def test_search_view(self):
        response = self.client.get(reverse('book:search'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/generic_product_list.html')

    def test_hot_offers_view(self):
        response = self.client.get(reverse('book:hot-offers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/generic_product_list.html')

    def test_tag_list_view(self):
        response = self.client.get(reverse('book:tag-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/author_tag_list.html')

    def test_author_list_view(self):
        response = self.client.get(reverse('book:author-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book/author_tag_list.html')
