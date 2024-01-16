from rest_framework.authentication import TokenAuthentication


class BearerTokenAuthentication(TokenAuthentication):
    """Overwriting the default class with keyword"""
    keyword = 'Bearer'
