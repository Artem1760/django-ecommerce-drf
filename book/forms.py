from django import forms
from django.core.exceptions import ValidationError

from .models import BookReview


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['star_rating', 'review']

    def clean_star_rating(self):
        star_rating = self.cleaned_data.get('star_rating')

        if star_rating is None or star_rating == 0:
            raise ValidationError('Please select a star rating.')

        return star_rating
