import auth_client


class BookTypeClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the BookTypeClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_type_list(self):
        """
        Retrieves a list of book types from the BookTypeListApiView.
        """
        # Endpoint for getting the list of types
        endpoint = "http://localhost:8000/api/v1/books/types/"
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

    def create_type(self, type_data):
        """
        Creates a Book Type instance using the BookTypeListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/types/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=type_data)

        if response.status_code == 201:
            data = response.json()
            print('Type was created successfully with details below:\n', data)
        else:
            print(
                f"Failed to create Type. Status code: {response.status_code}")

    def get_type(self, type_id):
        """
        Retrieves Type details from the BookTypeGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Type
        endpoint = f"http://localhost:8000/api/v1/books/type/{type_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Type with id {type_id}. "
                f"Status code: {response.status_code}")

    def update_type(self, type_id, updated_data):
        """
        Updates a Book Type using the BookTypeGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific Type
        endpoint = f"http://localhost:8000/api/v1/books/type/{type_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update Type details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(f"Type with id {type_id} updated successfully.\n",
                      updated_data)
            else:
                print(
                    f"Failed to update Type with id {type_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Type with id {type_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_type(self, type_id):
        """
        Deletes a Book Type using the BookTypeGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific Type
        endpoint = f"http://localhost:8000/api/v1/books/type/{type_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Type
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Type with id {type_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Type with id {type_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Type with id {type_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = BookTypeClient()

    # Examples
    # client.get_type_list()
    # client.create_type({'name': 'New Type Name'})
    # client.get_type(type_id)  # fill in type_id
    # client.update_type(type_id, {'name': 'Updated Type name'})   # fill in type_id
    # client.delete_type(type_id)   # fill in type_id
