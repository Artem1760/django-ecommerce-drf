import auth_client


class CategoryClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the CategoryClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_category_list(self):
        """
        Retrieves a list of categories from the CategoryListApiView.
        """
        # Endpoint for getting the list of categories
        endpoint = "http://localhost:8000/api/v1/books/categories/"
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

    def create_category(self, category_data):
        """
        Creates an Category instance using the CategoryListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/books/categories/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=category_data)

        if response.status_code == 201:
            data = response.json()
            print('Category was created successfully with details below:\n',
                  data)
        else:
            print(
                f"Failed to create Category. Status code: {response.status_code}")

    def get_category(self, category_id):
        """
        Retrieves Category details from the CategoryGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Category
        endpoint = f"http://localhost:8000/api/v1/books/category/{category_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Category with id {category_id}. "
                f"Status code: {response.status_code}")

    def update_category(self, category_id, updated_data):
        """
        Updates an Category using the CategoryGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific Category
        endpoint = f"http://localhost:8000/api/v1/books/category/{category_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update Category details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(
                    f"Category with id {category_id} updated successfully.\n",
                    updated_data)
            else:
                print(
                    f"Failed to update Category with id {category_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"Category with id {category_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_category(self, category_id):
        """
        Deletes an Category using the CategoryGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific Category
        endpoint = f"http://localhost:8000/api/v1/books/category/{category_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Category
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Category with id {category_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Category with id {category_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Category with id {category_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = CategoryClient()

    # Examples
    # client.get_category_list()
    # client.create_category({'name': 'New Category Name'})
    # client.get_category(category_id)  # fill in category_id
    # client.update_category(category_id, {'name': 'Updated Category name'})   # fill in category_id
    # client.delete_category(category_id)   # fill in category_id
