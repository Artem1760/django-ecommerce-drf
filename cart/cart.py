from decimal import Decimal

from django.conf import settings

from book.models import Book, BookLanguage, BookType
from checkout.models import DeliveryOptions


class Cart:
    """
    A base cart class, providing some default behaviors that
    can be inherited or overridden, as necessary.
    """

    def __init__(self, request):
        """
        Initialize the cart with the session data.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, book, quantity, language, book_type):
        """Add a book to the Cart"""
        book_id = str(book.id)

        if book_id in self.cart:
            # Update quantity and book details if the book is already in the cart
            self.cart[book_id]['quantity'] = quantity
            self.cart[book_id]['language_id'] = language.id
            self.cart[book_id]['book_type_id'] = book_type.id
        else:
            # Add new book to the cart
            self.cart[book_id] = {
                'price': str(
                    book.discount_price if book.discount_price else book.regular_price),
                'quantity': quantity,
                'language_id': language.id,
                'book_type_id': book_type.id
            }

        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart.
        """
        book_ids = self.cart.keys()

        # Initialize cart dictionary with all book_id entries
        cart = {
            str(book_id): {
                'quantity': self.cart[str(book_id)]['quantity'],
                'language_id': self.cart[str(book_id)]['language_id'],
                'book_type_id': self.cart[str(book_id)]['book_type_id'],
            } for book_id in book_ids
        }

        # Query books in a single database hit
        books = Book.objects.filter(id__in=book_ids)

        # Iterate over the books queried from the database
        for book in books:
            book_id_str = str(book.id)
            if book_id_str in cart:
                # Update the cart dictionary with book details
                cart[book_id_str]['book'] = book

                # Set the default price based on whether the book has a discount
                cart[book_id_str].setdefault('price',
                                             str(book.discount_price if book.discount_price else book.regular_price))

                # Set language and book type IDs from the existing cart data
                cart[book_id_str]['language_id'] = self.cart[book_id_str][
                    'language_id']
                cart[book_id_str]['book_type_id'] = self.cart[book_id_str][
                    'book_type_id']

        # Iterate over the values in the cart dictionary
        for item in cart.values():
            # Convert the 'price' value to a Decimal, defaulting to 0 if not present
            item['price'] = Decimal(item.get('price', 0))

            # Calculate the total price for the item (price * quantity)
            item['total_price'] = item['price'] * item['quantity']

            # Retrieve the corresponding BookLanguage and BookType objects based on the their IDs
            item['language_id'] = BookLanguage.objects.get(
                id=item['language_id'])
            item['book_type_id'] = BookType.objects.get(
                id=item['book_type_id'])
            yield item

    def __len__(self):
        """
        Get the cart data and count the quantity of items
        """
        return sum(item['quantity'] for item in self.cart.values())

    def update_quantity(self, book_id, quantity):
        """Update quantity in the Cart"""
        book_id_str = str(book_id)
        if book_id_str in self.cart:
            self.cart[book_id_str]['quantity'] = quantity
            self.save()

    def update_language(self, book_id, language_id):
        book_id_str = str(book_id)
        if book_id_str in self.cart:
            self.cart[book_id_str]['language_id'] = language_id
            self.save()

    def update_type(self, book_id, type_id):
        book_id_str = str(book_id)
        if book_id_str in self.cart:
            self.cart[book_id_str]['book_type_id'] = type_id
            self.save()

    def get_book_total_price(self, book_id):
        """Get the total price for a specific book in the cart."""
        book_id_str = str(book_id)

        if book_id_str in self.cart:
            book_data = self.cart[book_id_str]
            price = Decimal(book_data['price'])
            quantity = book_data['quantity']
            total_price = price * quantity
            return total_price

        return Decimal(0)

    def get_subtotal_price(self):
        """
        Get the subtotal price of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def get_delivery_option_id(self):
        """
        Get the delivery option ID from the session.
        """
        if 'purchase' in self.session:
            return self.session['purchase']['delivery_id']
        return None

    def get_delivery_price(self):
        """
        Get the delivery price based on the selected delivery option.
        """
        newprice = 0.00

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(
                id=self.session['purchase']['delivery_id']).delivery_price

        return newprice

    def get_total_price(self):
        """
        Get the total order price including the delivery cost.
        """
        newprice = 0.00
        subtotal = self.get_subtotal_price()

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(
                id=self.session['purchase']['delivery_id']).delivery_price

        total = subtotal + Decimal(newprice)
        return total

    def cart_update_delivery(self, delivery_price=0):
        """
        Update order total price with adding delivery cost.
        """
        subtotal = self.get_subtotal_price()
        total = subtotal + Decimal(delivery_price)
        return total

    def delete(self, book):
        """
        Delete item from session data
        """
        book_id = str(book.id) if isinstance(book, Book) else str(book)

        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def clear(self):
        """Remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        if 'purchase' in self.session:
            del self.session['purchase']
        self.save()

    def save(self):
        """
        Save the cart data to the session.
        """
        self.session.modified = True
