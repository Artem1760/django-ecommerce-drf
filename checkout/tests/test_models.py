from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from ..models import DeliveryOptions, Order, OrderItem, Address
from book.models import Book, BookLanguage, BookType, Category, Publisher, \
    Author


class BaseTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
                                                username='testuser',
                                                email='testuser@example.com',
                                                password='password')
        self.delivery_option = DeliveryOptions.objects.create(
            delivery_name='Express',
            delivery_price=10,
            is_active=True
        )
        self.book_language = BookLanguage.objects.create(language='English')
        self.book_type = BookType.objects.create(name='Hardcover')
        self.category = Category.objects.create(name='Test Category',
                                                slug='test-category',
                                                is_active=True)
        self.author = Author.objects.create(name='Test Author',
                                            slug='test-author')
        self.publisher = Publisher.objects.create(name='Test Publisher')

    def create_book(self):
        book = Book.objects.create(
            title='Test Book',
            slug='test-book',
            publication_date='2022-01-01',
            isbn=f'test-isbn-test-book',
            regular_price=Decimal('15.00'),
            is_sale=False,
            description=f'Test description for Test Book',
            quantity=50,
            created_date='2022-01-01',
            is_active=True,
            num_pages=200,
            category=self.category,
            author=self.author,
            publisher=self.publisher,
        )
        book.book_type.set([self.book_type])
        book.languages.set([self.book_language])
        return book


class DeliveryOptionsModelTest(BaseTest):
    def test_delivery_options_str(self):
        delivery_option = DeliveryOptions.objects.create(
            delivery_name='Express',
            delivery_price=10,
            is_active=True
        )
        self.assertEqual(str(delivery_option), 'Express')


class OrderModelTest(BaseTest):
    def test_order_str(self):
        order = Order.objects.create(
            user=self.user,
            oid='1234567890',
            total_price=Decimal('30.00'),
            delivery=self.delivery_option,
            transaction_id='abc123',
            payment_option='on_receive',
            billing_status=True,
            order_status='pending',
        )
        self.assertEqual(str(order),
                         f'Order {order.oid} by {self.user.username}')

    def test_get_total_cost(self):
        book = self.create_book()

        order = Order.objects.create(
            user=self.user,
            oid='1234567890',
            total_price=Decimal('30.00'),
            delivery=self.delivery_option,
            transaction_id='abc123',
            payment_option='on_receive',
            billing_status=True,
            order_status='pending',
        )
        OrderItem.objects.create(
            order=order,
            book=book,
            quantity=2,
            price=Decimal('15.00'),
            subtotal_price=Decimal('30.00'),
            language=self.book_language,
            book_type=self.book_type,
        )
        self.assertEqual(order.get_total_cost(), Decimal('30.00'))

    def test_formatted_shipping_address(self):
        address = Address.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john.doe@example.com',
            postcode='12345',
            country='US',
            street_address='123 Main St',
            town_city='Anytown',
            country_state='CA',
            delivery_instructions='Leave at the doorstep.',
            default=True,
        )
        order = Order.objects.create(
            user=self.user,
            oid='1234567890',
            total_price=Decimal('30.00'),
            delivery=self.delivery_option,
            transaction_id='abc123',
            payment_option='on_receive',
            billing_status=True,
            order_status='pending',
            shipping_address=address,
        )
        formatted_address = f'{address.first_name} {address.last_name}, ' \
                            f'{address.street_address}, {address.town_city}, ' \
                            f'{address.country}'
        self.assertEqual(order.formatted_shipping_address(), formatted_address)


class OrderItemModelTest(BaseTest):
    def test_order_item_str(self):
        book = self.create_book()

        order = Order.objects.create(
            user=self.user,
            oid='1234567899',
            total_price=Decimal('30.00'),
            delivery=self.delivery_option,
            transaction_id='abc123',
            payment_option='on_receive',
            billing_status=True,
            order_status='pending',
        )
        order_item = OrderItem.objects.create(
            order=order,
            book=book,
            quantity=2,
            price=Decimal('15.00'),
            subtotal_price=Decimal('30.00'),
            language=BookLanguage.objects.get(language='English'),
            book_type=BookType.objects.get(name='Hardcover'),
        )
        self.assertEqual(str(order_item), f'Order item: {order_item.id}')


class AddressModelTest(BaseTest):
    def test_address_str(self):
        address = Address.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            phone='1234567890',
            email='john.doe@example.com',
            postcode='12345',
            country='US',
            street_address='123 Main St',
            town_city='Anytown',
            country_state='CA',
            delivery_instructions='Leave at the doorstep.',
            default=True,
        )
        self.assertEqual(str(address), str(address.id))
