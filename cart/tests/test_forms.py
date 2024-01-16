from django.test import TestCase

from ..forms import AddToCartForm


class AddToCartFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            'book_id': 1,
            'book_qty': 2,
            'book_type_id': 1,
            'language_id': 1,
        }
        form = AddToCartForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_quantity(self):
        form_data = {
            'book_id': 1,
            'book_qty': 0,  # Invalid quantity
            'book_type_id': 1,
            'language_id': 1,
        }
        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['book_qty'],
                         ['Quantity must be greater than 0.'])

    def test_missing_language_and_type(self):
        form_data = {
            'book_id': 1,
            'book_qty': 2,
            # Missing book_type_id and language_id
        }
        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'],
                         ['Please select both language and type.'])

    def test_valid_quantity_and_missing_language_type(self):
        form_data = {
            'book_id': 1,
            'book_qty': 2,
            # Missing book_type_id and language_id
        }
        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['__all__'],
                         ['Please select both language and type.'])

    def test_invalid_quantity_and_missing_language_type(self):
        form_data = {
            'book_id': 1,
            'book_qty': 0,  # Invalid quantity
            # Missing book_type_id and language_id
        }
        form = AddToCartForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['book_qty'],
                         ['Quantity must be greater than 0.'])
        self.assertEqual(form.errors['__all__'],
                         ['Please select both language and type.'])
