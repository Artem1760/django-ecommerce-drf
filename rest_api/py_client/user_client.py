import auth_client


class UserClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the UserClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_user_list(self):
        """
        Retrieves a list of users from the UserListCreateApiView.
        """
        # Endpoint for getting the list of users
        endpoint = "http://localhost:8000/api/v1/users/"
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

    def create_user(self, user_data):
        """
        Creates an User instance using the UserListCreateApiView.
        """
        # Endpoint for creating a new author
        endpoint = "http://localhost:8000/api/v1/users/"
        response = self.make_authenticated_request('POST', endpoint,
                                                   data=user_data)

        if response.status_code == 201:
            data = response.json()
            print('User was created successfully with details below:\n', data)
        else:
            print(
                f"Failed to create User. Status code: {response.status_code}")

    def get_user(self, user_id):
        """
        Retrieves User details from the UserGetUpdateDestroyAPIView.       
        """
        # Endpoint for getting details of a specific User
        endpoint = f"http://localhost:8000/api/v1/user/{user_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve User with id {user_id}. "
                f"Status code: {response.status_code}")

    def update_user(self, user_id, updated_data):
        """
        Updates an User using the UserGetUpdateDestroyAPIView.
        """
        # Endpoint for updating details of a specific User
        endpoint = f"http://localhost:8000/api/v1/user/{user_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to update User details
            update_response = self.make_authenticated_request('PUT', endpoint,
                                                              data=updated_data)

            if update_response.status_code == 200:
                print(f"User with id {user_id} updated successfully.\n",
                      updated_data)
            else:
                print(
                    f"Failed to update User with id {user_id}. "
                    f"Status code: {update_response.status_code}")
        else:
            print(
                f"User with id {user_id} not found. "
                f"Status code: {get_response.status_code}")

    def delete_user(self, user_id):
        """
        Deletes an User using the UserGetUpdateDestroyAPIView.       
        """
        # Endpoint for deleting a specific User
        endpoint = f"http://localhost:8000/api/v1/user/{user_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the User
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"User with id {user_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete User with id {user_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"User with id {user_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = UserClient()

    # Examples
    # client.get_user_list()
    # client.create_user({ 
    #     'email': 'new@user.com',
    #     'username': 'created_new_user',
    #     'password': '3edcvfr4'
    #     })
    # client.get_user(user_id)  # fill in user_id
    # client.update_user(user_id, {
    # 'email': 'new@user.com',
    # 'username': 'updated_new_user',
    # 'password': '3edcvfr4',
    # 'first_name': 'New',
    # 'last_name': 'User'
    # })   # fill in user_id
    # client.delete_user(user_id)   # fill in user_id
