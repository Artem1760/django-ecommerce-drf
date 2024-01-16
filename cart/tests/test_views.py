from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from book.models import Book, BookLanguage, BookType, Category, Publisher, \
    Author, FilterPrice
from checkout.models import DeliveryOptions


class CartViewsTest(TestCase):
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

        # Create a request object with a session
        self.request = self.client.request().wsgi_request
        self.request.session.save()
        # Set a referrer in the HTTP header for testing
        self.referrer_url = reverse('core:index')
        # Add book to the Cart
        self.response = self.client.post(reverse('cart:cart-add'), {
            'book_id': self.book.id,
            'book_qty': 1,
            'book_type_id': self.book_type.id,
            'language_id': self.language.id,
        }, HTTP_REFERER=self.referrer_url)

    def test_cart_summary_view(self):
        response = self.client.get(reverse('cart:cart-summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertIn('cart', response.context)
        self.assertIn('title', response.context)
        self.assertIn('deliveries', response.context)

    def test_add_to_cart_view(self):
        self.assertRedirects(self.response, expected_url=self.referrer_url)

    def test_cart_update_view(self):
        # Update the quantity of the book in the cart
        self.response = self.client.post(reverse('cart:cart-update-delete'), {
            'action': 'update_cart',
            f'bookqty_{self.book.id}': 2,
        }, HTTP_REFERER=self.referrer_url)
        self.assertRedirects(self.response,
                             expected_url=reverse('cart:cart-summary'))

    def test_cart_delete_view(self):
        self.response = self.client.post(reverse('cart:cart-update-delete'), {
            'action': f'remove_item_{self.book.id}',
        }, HTTP_REFERER=self.referrer_url)
        self.assertRedirects(self.response,
                             expected_url=reverse('cart:cart-summary'))

    def test_cart_update_delete_view(self):
        # Update the quantity of the book in the cart
        self.response = self.client.post(reverse('cart:cart-update-delete'), {
            'action': 'update_cart',
        })
        self.assertRedirects(self.response,
                             expected_url=reverse('cart:cart-summary'))

        # Delete the book from the cart
        self.response = self.client.post(reverse('cart:cart-update-delete'), {
            'action': f'remove_item_{self.book.id}',
        }, HTTP_REFERER=self.referrer_url)
        self.assertRedirects(self.response,
                             expected_url=reverse('cart:cart-summary'))

    def test_cart_preview_delete_view(self):
        self.response = self.client.post(reverse('cart:cart-preview-delete'), {
            'remove_cart_item': str(self.book.id),
        }, HTTP_REFERER=self.referrer_url)
        self.assertRedirects(self.response, expected_url=self.referrer_url)
