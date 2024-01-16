import auth_client


class LanguageClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the LanguageClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_language_list(self):
        """
        Retrieves a list of languages from the LanguageListApiView.
        """
        # Endpoint for getting the list of languages
        endpoint = "http://localhost:8000/api/v1/books/languages/"
        response = self.make_authenticated_request('GET', endpoint)

        print(response.json())

        if response.status_code == 200:
            data = response.json()
            next_url = data.get('next')
            results = data.get('results')

            while next_url:
                # Make additional requests if there are more results
                get_response = self.make_authenticated_request('GET', next_url)
                data = get_response.json()
                next_url = data.get('next')
                results.extend(data.get('results'))

                print('next_url', next_url)
                print(results)

    def create_language(self, language_data):
        """
        Creates an Language instance using the LanguageListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/languages/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=language_data)

        if response.status_code == 201:
            data = response.json()
            print('Language was created successfully with details below:\n',
                  data)
        else:
            print(
                f"Failed to create Language. Status code: {response.status_code}")

    def get_language(self, language_id):
        """
        Retrieves Language details from the LanguageGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Language
        endpoint = f"http://localhost:8000/api/v1/books/language/{language_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Language with id {language_id}. "
                f"Status code: {response.status_code}")

    def update_language(self, language_id, updated_data):
        """
        Updates an Language using the LanguageGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific Language
        endpoint = f"http://localhost:8000/api/v1/books/language/{language_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update Language details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(
                    f"Language with id {language_id} updated successfully.\n",
                    updated_data)
            else:
                print(
                    f"Failed to update Language with id {language_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Language with id {language_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_language(self, language_id):
        """
        Deletes an Language using the LanguageGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific Language
        endpoint = f"http://localhost:8000/api/v1/books/language/{language_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Language
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Language with id {language_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Language with id {language_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Language with id {language_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = LanguageClient()

    # Examples
    # client.get_language_list()
    # client.create_language({'language': 'New Language Name'})
    # client.get_language(language_id)  # fill in language_id
    # client.update_language(language_id, {'language': 'Updated Language name'})   # fill in language_id
    # client.delete_language(language_id)   # fill in language_id
