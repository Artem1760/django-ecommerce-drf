from django.test import TestCase
from decimal import Decimal
from copy import deepcopy
from django.conf import settings
from django.contrib.auth import get_user_model

from book.models import Book, BookLanguage, BookType, Category, Author, \
    Publisher
from checkout.models import DeliveryOptions
from ..cart import Cart


class CartTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category',
                                                is_active=True)
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.publisher = Publisher.objects.create(name='Test Publisher')
        self.user = get_user_model().objects.create_user(username='testuser',
                                                         email='test@user.com',
                                                         password='testpassword', )
        self.language = BookLanguage.objects.create(language='English')
        self.book_type = BookType.objects.create(name='Fiction')
        self.delivery_option = DeliveryOptions.objects.create(
            delivery_name='Standard Delivery', delivery_price=5
        )
        # Create a book for testing
        self.book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            publication_date='2022-01-01',
            isbn='test-isbn-book',
            regular_price=50.00,
            discount_price=40.00,
            is_sale=True,
            description='Test description for Test Book',
            quantity=50,
            created_date='2022-01-01',
            is_active=True,
            num_pages=200,
            category=self.category,
            author=self.author,
            publisher=self.publisher,
        )

        # Create a request object with a session
        self.request = self.client.request().wsgi_request
        self.request.session.save()

    def test_add_book_to_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        # Check if the book is added to the cart
        self.assertIn(str(self.book.id), cart.cart)
        item = cart.cart[str(self.book.id)]
        self.assertEqual(item['quantity'], initial_quantity)
        self.assertEqual(item['language_id'], self.language.id)
        self.assertEqual(item['book_type_id'], self.book_type.id)

    def test_update_quantity_in_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        updated_quantity = 5
        cart.update_quantity(self.book.id, updated_quantity)

        # Check if the quantity is updated in the cart
        item = cart.cart[str(self.book.id)]
        self.assertEqual(item['quantity'], updated_quantity)

    def test_update_language_in_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        new_language = BookLanguage.objects.create(language='Spanish')
        cart.update_language(self.book.id, new_language.id)

        # Check if the language is updated in the cart
        item = cart.cart[str(self.book.id)]
        self.assertEqual(item['language_id'], new_language.id)

    def test_update_type_in_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        new_type = BookType.objects.create(name='Non-Fiction')
        cart.update_type(self.book.id, new_type.id)

        # Check if the book type is updated in the cart
        item = cart.cart[str(self.book.id)]
        self.assertEqual(item['book_type_id'], new_type.id)

    def test_delete_book_from_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        cart.delete(self.book)

        # Check if the book is removed from the cart
        self.assertNotIn(str(self.book.id), cart.cart)

    def test_clear_cart(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        cart.clear()

        # Check if the cart is cleared
        self.assertNotIn(settings.CART_SESSION_ID, self.request.session)
        self.assertNotIn('purchase', self.request.session)

    def test_get_book_total_price(self):
        cart = Cart(self.request)
        initial_quantity = 3
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        total_price = cart.get_book_total_price(self.book.id)

        # Check if the total price for the book is correct
        expected_price = Decimal(self.book.discount_price) * initial_quantity
        self.assertEqual(total_price, expected_price)

    def test_get_subtotal_price(self):
        cart = Cart(self.request)
        initial_quantity_1 = 2
        initial_quantity_2 = 3
        book_1 = self.book  # book 1 instance
        book_2 = deepcopy(self.book)  # book 2 instance
        book_2.id = 5136890885
        book_2.title = 'Book 2'
        book_2.isbn = 'isbn1234567890'
        book_2.slug = 'book-2'
        book_2.regular_price = 20.00
        book_2.discount_price = 15.00
        book_2.save()

        cart.add(book_1, initial_quantity_1, self.language, self.book_type)
        cart.add(book_2, initial_quantity_2, self.language, self.book_type)

        subtotal_price = cart.get_subtotal_price()

        # Check if the subtotal price is correct
        expected_subtotal = (
                Decimal(book_1.discount_price) * initial_quantity_1
                + Decimal(book_2.discount_price) * initial_quantity_2
        )

        self.assertEqual(subtotal_price, expected_subtotal)

    def test_get_delivery_option_id(self):
        cart = Cart(self.request)
        self.request.session['purchase'] = {
            'delivery_id': self.delivery_option.id}

        delivery_id = cart.get_delivery_option_id()

        # Check if the correct delivery option ID is retrieved from the session
        self.assertEqual(delivery_id, self.delivery_option.id)

    def test_get_delivery_price(self):
        cart = Cart(self.request)
        self.request.session['purchase'] = {
            'delivery_id': self.delivery_option.id}

        delivery_price = cart.get_delivery_price()

        # Check if the correct delivery price is retrieved based on the selected delivery option
        self.assertEqual(delivery_price,
                         Decimal(self.delivery_option.delivery_price))

    def test_get_total_price(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)
        self.request.session['purchase'] = {
            'delivery_id': self.delivery_option.id}

        total_price = cart.get_total_price()

        # Check if the correct total order price is calculated including the delivery cost
        expected_total = (
                Decimal(self.book.discount_price) * initial_quantity
                + Decimal(self.delivery_option.delivery_price)
        )
        self.assertEqual(total_price, expected_total)

    def test_cart_update_delivery(self):
        cart = Cart(self.request)
        initial_quantity = 2
        cart.add(self.book, initial_quantity, self.language, self.book_type)

        updated_total_price = cart.cart_update_delivery(delivery_price=5.00)

        # Check if the order total price is updated with the added delivery cost
        expected_total = Decimal(
            self.book.discount_price) * initial_quantity + Decimal(5.00)
        self.assertEqual(updated_total_price, expected_total)
