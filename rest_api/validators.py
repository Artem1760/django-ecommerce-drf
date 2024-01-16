from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from book.models import (Author, Book, BookLanguage,
                         BookType, Category, Publisher)


def validate_required_field(value, field_name):
    """Validate that a required field is not empty or None."""
    if not value:
        raise serializers.ValidationError(f"{field_name} field is required.")
    return value


def validate_text_len(value):
    """Custom validator to ensure that the text length is not too short."""
    if len(value) < 3:
        raise serializers.ValidationError(
            'Text should be at least 3 characters long.')
    return value


def validate_num_zero(value):
    """Custom validator to ensure that the number is greater than zero."""
    if value <= 0:
        raise serializers.ValidationError("Number must be greater than zero.")
    return value


def validate_sale_and_discount(data):
    """If is_sale is True, discount_price is required, and vice versa."""
    is_sale = data.get('is_sale', False)
    discount_price = data.get('discount_price', None)

    # Both fields must be present or both must be absent
    if (is_sale and discount_price is None) or (
            not is_sale and discount_price is not None):
        raise serializers.ValidationError({
            'is_sale': 'If is_sale is True, discount_price is required, and vice versa.'
        })


def validate_discount_price(data):
    """
    Custom validator to ensure that the discount price is lower than the regular price.
    """
    regular_price = data.get('regular_price')
    discount_price = data.get('discount_price')

    if discount_price is not None and \
            regular_price is not None and \
            discount_price >= regular_price:
        raise serializers.ValidationError({
            'discount_price': [
                "Discount price must be lower than the regular price."]
        })
    return discount_price


# Validate if the field value is unique
unique_author_name = UniqueValidator(queryset=Author.objects.all(),
                                     lookup='iexact')
unique_category_name = UniqueValidator(queryset=Category.objects.all(),
                                       lookup='iexact')
unique_book_type = UniqueValidator(queryset=BookType.objects.all(),
                                   lookup='iexact')
unique_publisher_name = UniqueValidator(queryset=Publisher.objects.all(),
                                        lookup='iexact')
unique_language = UniqueValidator(queryset=BookLanguage.objects.all(),
                                  lookup='iexact')
unique_book_title = UniqueValidator(queryset=Book.objects.all(),
                                    lookup='iexact')
