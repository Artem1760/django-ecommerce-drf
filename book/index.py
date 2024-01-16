from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register

from .models import Book


# Indexes for algolia search


@register(Book)
class BookIndex(AlgoliaIndex):
    """
    Configure the index Algolia custom model based on the model BookReview.
    """
    # fields to display
    fields = ['id', 'title', 'description', 'publication_date',
              'regular_price', 'discount_price', 'quantity', 'created_date',
              'is_active', 'num_pages', 'category',
              'author', 'publisher']
    settings = {
        # attributes to search in   
        'searchableAttributes': ['title', 'author', 'publisher'],
        # use category as a searching parameter: &category=humor     
        'attributesForFaceting': ['is_active', 'category']
    }


"""
Use the following Python commands to manage your Algolia indices:

* python manage.py algolia_reindex: reindex all the registered models. 
  This command first sends all records to a temporary index and then moves it. 
  Pass --model as a parameter to reindex a specific model
- python manage.py algolia_applysettings: apply or reapply the index settings.
- python manage.py algolia_clearindex: clear the index
"""
