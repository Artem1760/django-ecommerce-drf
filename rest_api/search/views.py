# algolia_views.py

from rest_framework import generics
from rest_framework.response import Response

from . import client


class SearchListView(generics.GenericAPIView):
    """We use this view for ALGOLIA search api"""

    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        is_active_book = str(request.GET.get('is_active')) != "0"
        category = request.GET.get('category')

        if not query:
            return Response('No Results...', status=400)
        results = client.search(query, category=category,
                                is_active=is_active_book)
        return Response(results)
