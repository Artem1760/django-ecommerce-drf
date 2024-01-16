from django import forms
from django.core.exceptions import ValidationError


class AddToCartForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())
    book_qty = forms.IntegerField()
    book_type_id = forms.IntegerField()
    language_id = forms.IntegerField()

    def clean_book_qty(self):
        book_qty = self.cleaned_data.get('book_qty')
        if book_qty is not None and book_qty <= 0:
            raise ValidationError('Quantity must be greater than 0.')
        return book_qty

    def clean(self):
        """
        Check selection of the language_id and 
        book_type_id before adding to the Cart
        """
        cleaned_data = super().clean()
        language_id = cleaned_data.get('language_id')
        book_type_id = cleaned_data.get('book_type_id')

        if not (language_id and book_type_id):
            raise ValidationError('Please select both language and type.')
        return cleaned_data
