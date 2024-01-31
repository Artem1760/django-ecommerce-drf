# Book Store Project

Welcome to the Book Store Project! This Django-based project serves as an online book store, providing a seamless experience for both administrators and users. The project is organized into several Django apps, each catering to specific functionalities:

- **book**: This app manages book-related models, including `Book`, `Category`, and others.
- **cart**: Responsible for handling the shopping cart logic, enabling users to add, modify, and finalize their book selections.
- **checkout**: Manages the entire checkout process, from order creation to payment handling, ensuring a smooth transaction for users.
- **core**: This app encapsulates the core functionalities, covering the homepage, about us, and contact pages.
- **account**: Manages user-related functionalities, including custom user creation with email confirmation for enhanced security and personalized services. Additionally, this app maintains contact information for efficient communication.

## Django Rest Framework Integration

The Book Store Project now incorporates Django Rest Framework (DRF) to provide a robust API for CRUD operations on various models. Here are some key features related to DRF:

- **API Endpoints**: The project exposes API endpoints for all relevant models, allowing users to Create, Read, Update, and Delete instances using standard HTTP methods.

- **Token Authentication**: Token-based authentication is implemented using the Djoser package, ensuring secure access to API endpoints. Users can obtain authentication tokens for accessing protected resources.

- **Permissions and Validations**: DRF permissions are utilized to control access to specific API views based on user roles. Validations ensure data integrity and consistency.

- **Mixins for Functionality**: DRF mixins are employed to enhance functionality in views, providing common behavior such as creating and updating instances.

- **Search with Django Algolia**: Django Algolia implements efficient and fast search functionality. Users can easily search for specific book, author, publisher or other relevant information, enhancing the overall user experience.

### Installation

To get started with this project, follow these steps:

1. Clone the Repository
    Clone the repository to your local machine:
        ```bash
        git clone https://github.com/Artem1760/django-ecommerce-drf.git
        ```
2. Navigate to the project directory: `cd <project-directory>`
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - On Windows:
        ```bash
        source venv/Scripts/activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
5. Install dependencies: `pip install -r requirements.txt`
6. Activate the provided PostgreSQL database:
    - Use password for db from .env file:    
    ```bash
    pg_restore --dbname=book_store --username=djcrmuser --password=your_password ./book_store_db.sql
    ```  
7. Set environment variables in the `.env` file (see below)
8. Apply migrations: `python manage.py migrate`
9. Run the development server: `python manage.py runserver`
10. Create a superuser to access the admin panel: `python manage.py createsuperuser`

### Environment Variables (.env)
Replace environment variables in the `.env` file in the project root with your preferred values.



## Usage

1. Navigate to the homepage at `http://localhost:8000/` to browse and explore available books.
2. Add desired books to the shopping cart for a personalized selection.
3. Proceed to checkout, where you can conveniently choose delivery options and your preferred payment method.
4. Manage and review orders through the admin panel.

## Features and Functionality

📌 **Custom User Model**: The project utilizes a custom user model to extend the user functionality and capture additional details.

📌 **Unit Tests**: The application includes unit tests to ensure the reliability and functionality of its components.

📌 **Static Assets**: The project manages static assets efficiently, ensuring optimal performance and responsiveness.

📌 **Advanced User Registration**: Users can register and create accounts using the DRF API, enhancing their shopping experience and providing personalized services. Token authentication ensures secure access to user-related endpoints.

📌 **Environment Variables**: Sensible data is managed using environment variables, ensuring security and configurability.

📌 **Email Services**: The application integrates email services for user communication, order confirmations, and other notifications.

📌 **Reviews App**: Users can leave reviews for books, contributing to a dynamic and interactive platform.

📌 **Image Uploads**: The project supports image uploads for books and user profiles, enhancing visual appeal.

📌 **Permissions**: Role-based permissions ensure secure access and actions based on user roles for drf part of the project.

📌 **Search**: The search functionality allows users to find specific books efficiently with Algolia for drf part and basic filtering Q objects in the search form for main part of the django project.

📌 **Py Client for DRF**: Py Clients provide a convenient interface for interacting with the Django Rest Framework (DRF) API related to the models in the Book Store Project. It allows users to retrieve a list of instances, create new ones, get, update, and delete, enhancing the ease of managing model data through the DRF endpoints.

📌 **Shopping Cart Sessions**: The shopping cart sessions persist across user sessions, allowing for a seamless shopping experience.

## Contributing

Feel free to contribute to this project by forking the repository, making necessary changes, and submitting a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.







