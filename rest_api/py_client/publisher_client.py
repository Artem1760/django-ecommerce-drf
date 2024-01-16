import auth_client


class PublisherClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the PublisherClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_publisher_list(self):
        """
        Retrieves a list of publishers from the PublisherListApiView.
        """
        # Endpoint for getting the list of publishers
        endpoint = "http://localhost:8000/api/v1/books/publishers/"
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

    def create_publisher(self, publisher_data):
        """
        Creates an Publisher instance using the LanguageListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/publishers/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=publisher_data)

        if response.status_code == 201:
            data = response.json()
            print('Publisher was created successfully with details below:\n',
                  data)
        else:
            print(
                f"Failed to create Publisher. Status code: {response.status_code}")

    def get_publisher(self, publisher_id):
        """
        Retrieves Publisher details from the PublisherGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Publisher
        endpoint = f"http://localhost:8000/api/v1/books/publisher/{publisher_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Publisher with id {publisher_id}. "
                f"Status code: {response.status_code}")

    def update_publisher(self, publisher_id, updated_data):
        """
        Updates an Publisher using the PublisherGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific Publisher
        endpoint = f"http://localhost:8000/api/v1/books/publisher/{publisher_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update Publisher details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(
                    f"Publisher with id {publisher_id} updated successfully.\n",
                    updated_data)
            else:
                print(
                    f"Failed to update Publisher with id {publisher_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Publisher with id {publisher_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_publisher(self, publisher_id):
        """
        Deletes an Publisher using the PublisherGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific Publisher
        endpoint = f"http://localhost:8000/api/v1/books/publisher/{publisher_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Publisher
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(
                    f"Publisher with id {publisher_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Publisher with id {publisher_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Publisher with id {publisher_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = PublisherClient()

    # Examples
    client.get_publisher_list()
    # client.create_publisher({'name': 'New Publisher Name'})
    # client.get_publisher(publisher_id)  # fill in publisher_id
    # client.update_publisher(publisher_id, {'name': 'Updated Publisher name'})   # fill in publisher_id
    # client.delete_publisher(publisher_id)   # fill in publisher_id
