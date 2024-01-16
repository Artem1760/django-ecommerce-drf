import auth_client


class AuthorClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the AuthorClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_author_list(self):
        """
        Retrieves a list of authors from the AuthorListApiView.
        """
        # Endpoint for getting the list of authors
        endpoint = "http://localhost:8000/api/v1/books/authors/"
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

    def create_author(self, author_data):
        """
        Creates an author instance using the AuthorListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/authors/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=author_data)

        if response.status_code == 201:
            data = response.json()
            print('Author was created successfully with details below:\n',
                  data)
        else:
            print(
                f"Failed to create Author. Status code: {response.status_code}")

    def get_author(self, author_id):
        """
        Retrieves author details from the AuthorGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific author
        endpoint = f"http://localhost:8000/api/v1/books/author/{author_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Author with id {author_id}. "
                f"Status code: {response.status_code}")

    def update_author(self, author_id, updated_data):
        """
        Updates an author using the AuthorGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific author
        endpoint = f"http://localhost:8000/api/v1/books/author/{author_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update author details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(f"Author with id {author_id} updated successfully.\n",
                      updated_data)
            else:
                print(
                    f"Failed to update Author with id {author_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Author with id {author_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_author(self, author_id):
        """
        Deletes an author using the AuthorGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific author
        endpoint = f"http://localhost:8000/api/v1/books/author/{author_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the author
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Author with id {author_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Author with id {author_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Author with id {author_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = AuthorClient()

    # Examples
    # client.get_author_list()
    # client.create_author({'name': 'New Author Name'})
    # client.get_author(author_id)  # fill in author_id
    # client.update_author(author_id, {'name': 'Updated author name'})   # fill in author_id
    # client.delete_author(author_id)   # fill in author_id
