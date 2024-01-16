import auth_client


class OrderClient(auth_client.BaseAuthenticatedClient):
    """
    Initializes the OrderClient and authenticates the user.
    """

    def __init__(self):
        super().__init__()

    def get_order_list(self):
        """
        Retrieves a list of orders from the OrderListApiView.
        """
        # Endpoint for getting the list of categories
        endpoint = "http://localhost:8000/api/v1/orders/"
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

    def get_order(self, order_id):
        """
        Retrieves Order details from the OrderGetDestroyAPIView.       
        """
        # Endpoint for getting details of a specific Order
        endpoint = f"http://localhost:8000/api/v1/order/{order_id}/"
        response = self.make_authenticated_request('GET', endpoint)

        if response.status_code == 200:
            data = response.json()
            print(data)
        else:
            print(
                f"Failed to retrieve Order with id {order_id}. "
                f"Status code: {response.status_code}")

    def delete_order(self, order_id):
        """
        Deletes an Order using the OrderGetDestroyAPIView.       
        """
        # Endpoint for deleting a specific Order
        endpoint = f"http://localhost:8000/api/v1/order/{order_id}/"
        get_response = self.make_authenticated_request('GET', endpoint)

        if get_response.status_code == 200:
            # Make request to delete the Order
            delete_response = self.make_authenticated_request('DELETE',
                                                              endpoint)

            if delete_response.status_code == 204:
                print(f"Order with id {order_id} deleted successfully.")
            else:
                print(
                    f"Failed to delete Order with id {order_id}. "
                    f"Status code: {delete_response.status_code}")
        else:
            print(
                f"Order with id {order_id} not found. "
                f"Status code: {get_response.status_code}")


if __name__ == '__main__':
    client = OrderClient()

    # Examples
    # client.get_order_list()  
    # client.get_order(order_id)  # fill in order_id   
    # client.delete_order(10)   # fill in order_id
