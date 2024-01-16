from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from book.models import Book, BookLanguage, BookType, Category, Publisher, \
    Author, FilterPrice
from checkout.models import DeliveryOptions


class CartURLTests(TestCase):
    def setUp(self):
        # Create a user for testing login_required view
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         email='test@user.com',
                                                         password='testpassword')

        # Create some sample data for testing
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category')
        self.language = BookLanguage.objects.create(language='English')
        self.book_type = BookType.objects.create(name='Fiction')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.filter_price = FilterPrice.objects.create(price='Under $25')
        self.delivery_option = DeliveryOptions.objects.create(
            delivery_name='Standard', delivery_price=5, is_active=True)

        self.book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            publication_date='2023-01-01',
            isbn='test-isbn',
            regular_price=20,
            discount_price=15,
            is_sale=True,
            cover='book_covers/test-cover.jpg',
            description='Test description',
            specification='Test specification',
            quantity=50,
            num_pages=200,
            category=self.category,
            author=self.author,
            publisher=self.publisher,
            filter_price=self.filter_price
        )

        # Set a referrer in the HTTP header for testing
        self.referrer_url = reverse('core:index')

    def test_cart_summary_url(self):
        url = reverse('cart:cart-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_url(self):
        self.client.force_login(self.user)
        url = reverse('cart:cart-add')
        response = self.client.post(url, {
            'book_id': self.book.id,
            'book_qty': 1,
            'book_type_id': self.book_type.id,
            'language_id': self.language.id,
        }, HTTP_REFERER=self.referrer_url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_cart_update_delete_url(self):
        # Test the 'update_cart' action
        url = reverse('cart:cart-update-delete')
        response = self.client.post(url, {'action': 'update_cart'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

        # Test the 'remove_item_' action
        response = self.client.post(url,
                                    {'action': f'remove_item_{self.book.id}'})
        self.assertEqual(response.status_code, 302)  # Expecting a redirect

    def test_cart_preview_delete_url(self):
        url = reverse('cart:cart-preview-delete')
        response = self.client.post(url, {'remove_cart_item': self.book.id},
                                    HTTP_REFERER=self.referrer_url)
        self.assertEqual(response.status_code, 302)  # Expecting a redirect
