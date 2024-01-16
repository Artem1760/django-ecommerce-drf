import requests
from getpass import getpass


class BaseAuthenticatedClient:
    """Authenticates the user"""

    def __init__(self):
        self.auth_token = self.authenticate()

    def authenticate(self):
        """
        Authenticates the user and returns the auth token.

        Returns:
            str: Auth token if authentication is successful, otherwise None.
        """
        # Authentication endpoint
        auth_endpoint = "http://localhost:8000/auth/token/login/"
        email = input('Email: \n')
        password = getpass('What is your password? \n')

        # Make authentication request
        auth_response = requests.post(auth_endpoint, json={'email': email,
                                                           'password': password})

        print(auth_response.json())

        if auth_response.status_code == 200:
            return auth_response.json()['auth_token']
        else:
            print(
                f"Authentication failed. Status code: {auth_response.status_code}")
            return None

    def make_authenticated_request(self, method, endpoint, data=None):
        """
        Makes an authenticated HTTP request to the given endpoint.

        Args:
            method (str): HTTP method (GET, POST, PUT, DELETE, etc.).
            endpoint (str): URL endpoint to make the request to.
            data (dict): Data to be included in the request body for POST and PUT requests.

        Returns:
            requests.Response: Response object.
        """
        # Include authentication token in the request headers
        headers = {'Authorization': f"Bearer {self.auth_token}"}
        response = requests.request(method, endpoint, headers=headers, json=data)

        return response
