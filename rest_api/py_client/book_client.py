import auth_client


class BookClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the BookClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_book_list(self):
        """
        Retrieves a list of books from the BookListCreateApiView.
        """
        # Endpoint for getting the list of books
        endpoint = "http://localhost:8000/api/v1/books/"
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

    def create_book(self, book_data):
        """
        Creates an Book instance using the BookListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=book_data)

        if response.status_code == 201:
            data = response.json()
            print('Book was created successfully with details below:\n', data)
        else:
            print(
                f"Failed to create Book. Status code: {response.status_code}")

    def get_book(self, book_id):
        """
        Retrieves Book details from the BookGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Book
        endpoint = f"http://localhost:8000/api/v1/book/{book_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Book with id {book_id}. "
                f"Status code: {response.status_code}")

    def update_book(self, book_id, updated_data):
        """
        Updates an Book using the BookGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific Book
        endpoint = f"http://localhost:8000/api/v1/book/{book_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update Book details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(f"Book with id {book_id} updated successfully.\n",
                      updated_data)
            else:
                print(
                    f"Failed to update Book with id {book_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Book with id {book_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_book(self, book_id):
        """
        Deletes an Book using the BookGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific Book
        endpoint = f"http://localhost:8000/api/v1/book/{book_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Book
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Book with id {book_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Book with id {book_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Book with id {book_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = BookClient()

    # Examples
    # client.get_book_list()
    # client.create_book({
    #                     'title': 'Created New Book',
    #                     'publication_date': '2023-11-07',
    #                     'regular_price': 24.00,  
    #                     'quantity': 12,            
    #                     'is_active': False,
    #                     'num_pages': 342,
    #                     'category': 'Art',
    #                     'author': 'Dolly Alderton',
    #                     'book_type': ['Kindle'],
    #                     'publisher': 'Penguin Press',
    #                     'languages': ['Ukrainian'],
    #                     'filter_price': 'Under $25'
    #                 })

    # client.get_book(book_id)  # fill in book_id
    # client.update_book(book_id, {
    #                             'title': 'Updated New Book',
    #                             'publication_date': '2023-11-07',
    #                             'regular_price': 20.00,  
    #                             'quantity': 10,            
    #                             'is_active': False,
    #                             'num_pages': 342,
    #                             'category': 'Art',
    #                             'author': 'Dolly Alderton',
    #                             'book_type': ['Kindle'],
    #                             'publisher': 'Penguin Press',
    #                             'languages': ['English'],
    #                             'filter_price': 'Under $25'
    #                     })   # fill in book_id
    # client.delete_book(book_id)   # fill in book_id
