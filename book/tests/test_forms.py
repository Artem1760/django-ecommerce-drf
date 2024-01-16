from django.forms import ValidationError
from django.test import TestCase
from ..forms import BookReviewForm
from ..models import Book, Author, Category, Publisher


class BookReviewFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category',
                                                is_active=True)
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            publication_date='2022-01-01',
            isbn='test-isbn',
            regular_price=20.00,
            is_sale=False,
            description='Test description',
            quantity=50,
            created_date='2022-01-01',
            is_active=True,
            num_pages=200,
            category=self.category,
            author=self.author,
            publisher=self.publisher,
        )

    def test_book_review_form_valid(self):
        form_data = {
            'star_rating': 4,
            'review': 'Great book!',
        }
        form = BookReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_book_review_form_invalid_star_rating(self):
        form_data = {
            'star_rating': 0,
            'review': 'This book is not good.',
        }
        form = BookReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

        # Update the assertion to check for the part of the error message that matches
        self.assertIn(
            'Select a valid choice. 0 is not one of the available choices.',
            form.errors['star_rating'][0])

    def test_book_review_form_invalid_missing_fields(self):
        form_data = {}
        form = BookReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['star_rating'][0])
        self.assertIn('This field is required.', form.errors['review'][0])

    def test_clean_star_rating_invalid_zero(self):
        data = {'star_rating': 0}
        form = BookReviewForm(data=data)
        with self.assertRaisesMessage(ValidationError,
                                      'Please select a star rating.'):
            form.is_valid()  # This will populate cleaned_data
            form.clean_star_rating()

    def test_clean_star_rating_invalid_none(self):
        data = {'star_rating': None}
        form = BookReviewForm(data=data)
        with self.assertRaisesMessage(ValidationError,
                                      'Please select a star rating.'):
            form.is_valid()  # This will populate cleaned_data
            form.clean_star_rating()
