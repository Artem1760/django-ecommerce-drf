from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth import get_user_model

from ..models import (BookType, Category, Book, BookImage, BookLanguage,
                      Publisher, Author, BookReview, FilterPrice)


class BaseModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category',
                                                is_active=True)
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         email='test@user.com',
                                                         password='testpassword')

    def create_book(self, title='Test Book', is_sale=False):
        return Book.objects.create(
            title=title,
            slug='test-book',
            publication_date='2022-01-01',
            isbn='test-isbn-test-book',
            regular_price=20.00,
            is_sale=is_sale,
            description='Test description for Test Book',
            quantity=50,
            created_date='2022-01-01',
            is_active=True,
            num_pages=200,
            category=self.category,
            author=self.author,
            publisher=self.publisher,
        )

    def create_book_review(self, book, rating=4, review='Test Review'):
        return BookReview.objects.create(book=book, user=self.user,
                                         star_rating=rating, review=review)


class CategoryModelTest(BaseModelTest):
    def test_category_name(self):
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_get_absolute_url(self):
        self.assertEqual(self.category.get_absolute_url(),
                         '/shop/categories/test-category/')

    def test_category_get_book_count(self):
        self.assertEqual(self.category.get_book_count(), 0)


class BookTypeModelTest(TestCase):
    def test_book_type_name(self):
        book_type = BookType.objects.create(name='Test Book Type')
        self.assertEqual(str(book_type), 'Test Book Type')


class BookModelTest(BaseModelTest):
    def test_book_title(self):
        book = self.create_book()
        self.assertEqual(str(book), 'Test Book')

    def test_book_get_absolute_url(self):
        book = self.create_book()
        self.assertEqual(book.get_absolute_url(), f'/shop/books/{book.slug}/')

    def test_book_get_percentage(self):
        book = self.create_book(is_sale=True)
        self.assertEqual(book.get_percentage(), 100)

    def test_book_average_star_rating(self):
        book = self.create_book()
        self.assertEqual(book.average_star_rating(), 0)

    def test_book_book_search(self):
        book = self.create_book()
        search_results = Book.book_search('test query')
        self.assertEqual(search_results.count(), 1)


class BookImageModelTest(BaseModelTest):
    def test_book_image_get_absolute_url(self):
        book = self.create_book()
        book_image = BookImage.objects.create(book=book, is_feature=True)
        self.assertEqual(book_image.get_absolute_url(), f'/shop/books/1/')


class BookLanguageModelTest(TestCase):
    def test_book_language_name(self):
        book_language = BookLanguage.objects.create(language='English')
        self.assertEqual(str(book_language), 'English')


class PublisherModelTest(TestCase):
    def test_publisher_name(self):
        publisher = Publisher.objects.create(name='Test Publisher')
        self.assertEqual(str(publisher), 'Test Publisher')


class AuthorModelTest(BaseModelTest):
    def test_author_name(self):
        self.assertEqual(str(self.author), 'Test Author')

    def test_author_get_absolute_url(self):
        self.assertEqual(self.author.get_absolute_url(),
                         f'/shop/books/author/{self.author.slug}/')

    def test_author_get_book_count(self):
        self.assertEqual(self.author.get_book_count(), 0)


class BookReviewModelTest(BaseModelTest):
    def test_book_review_str(self):
        book = self.create_book()
        book_review = self.create_book_review(book)
        self.assertEqual(str(book_review), 'Test Review')

    def test_book_review_clean_invalid_rating(self):
        book = self.create_book()
        book_review = self.create_book_review(book, rating=0)
        with self.assertRaises(ValidationError):
            book_review.clean()


class FilterPriceModelTest(TestCase):
    def test_filter_price_str(self):
        filter_price = FilterPrice.objects.create(price='Under $25')
        self.assertEqual(str(filter_price), 'Under $25')
