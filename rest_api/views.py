from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from checkout.models import Order
from .authentication import BearerTokenAuthentication
from django.contrib.auth import get_user_model

from book.models import BookLanguage, BookReview, Book, BookType, Author, \
    Category, Publisher
from .permissions import IsAdminOrReadOnly
from .serializers import (BookLanguageSerializer, BookReviewSerializer,
                          BookReviewDetailSerializer,
                          UserDetailSerializer, UserListSerializer,
                          BookSerializer,
                          BookDetailSerializer, CategorySerializer,
                          BookTypeSerializer,
                          PublisherSerializer, AuthorSerializer,
                          OrderSerializer, OrderDetailSerializer)
from .mixins import UserQuerySetMixin, StaffEditorPermissionMixin


############ Custom Pagination ############
class CustomAPIListPagination(PageNumberPagination):
    """Custom pagination class for API lists."""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10


############ User ###########
class UserListCreateApiView(StaffEditorPermissionMixin,
                            generics.ListCreateAPIView):
    """
    API view for listing and creating users.
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserListSerializer
    pagination_class = CustomAPIListPagination
    authentication_classes = [BearerTokenAuthentication]

    def create(self, request, *args, **kwargs):
        """
        Create a new user.

        Args:
            request (Request): The request object containing user data.
            args: Additional arguments passed to the method.
            kwargs: Additional keyword arguments passed to the method.

        Returns:
            Response: The response containing the serialized user data.

        Raises:
            ValidationError: If the provided data is invalid.
        """
        password = request.data.get('password')
        is_active = request.data.get('is_active', True)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.perform_create(serializer, password, is_active)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)

    def perform_create(self, serializer, password, is_active):
        """
        Perform the creation of a new user.

        Args:
            serializer (Serializer): The serializer instance.
            password (str): The password for the new user.
            is_active (bool): The value for the 'is_active' field.

        Returns:
            User: The created user instance.
        """
        user = serializer.save()

        # Set the password using set_password to ensure it's hashed
        if password:
            user.set_password(password)
            user.save()

        # Set the is_active field
        user.is_active = is_active
        user.save()

        return user


class UserGetUpdateDestroyAPIView(StaffEditorPermissionMixin,
                                  generics.RetrieveUpdateDestroyAPIView):
    """"
    API view for retrieving, updating, and deleting user data
    with permissions only for admin.
    """
    queryset = get_user_model().objects
    serializer_class = UserDetailSerializer
    authentication_classes = [BearerTokenAuthentication]


################## Book ####################
class BookTypeListApiView(generics.ListCreateAPIView):
    """
    API view for listing all book types and creating
    new one with admin permission.
    """
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()


class BookTypeGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting details of
    a book type with admin permission.
    """
    queryset = BookType.objects.all()
    serializer_class = BookTypeSerializer
    permission_classes = (IsAdminOrReadOnly,)


class LanguageListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all book languages and
    creating new one with admin permission.
    """
    queryset = BookLanguage.objects.all()
    serializer_class = BookLanguageSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()


class LanguageGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting details
    of a book language with admin permission.
    """
    queryset = BookLanguage.objects.all()
    serializer_class = BookLanguageSerializer
    permission_classes = (IsAdminOrReadOnly,)


class CategoryListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all categories and
    creating new one with admin permission.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()


class CategoryGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting
    details of a category with admin permission.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class PublisherListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all publishers and creating
    new one with admin permission.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save()


class PublisherGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting details
    of a publisher with admin permission.
    """
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AuthorListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all authors and creating new authors
    with admin permission.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        name = serializer.validated_data.get('name')
        if name:
            serializer.validated_data['name'] = name.title()
        serializer.save()


class AuthorGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting details
    of an author with admin permission.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsAdminOrReadOnly,)


class BookListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all books and creating
    new books with admin permission.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        description_default = 'Default Book Description'
        specification_default = 'Default Book Specification'

        serializer.save(
            description=description_default,
            specification=specification_default
        )


class BookGetUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view for retrieving, updating, and deleting details
    of a book with admin permission.
    """
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)
    authentication_classes = [BearerTokenAuthentication]


class ReviewListCreateApiView(generics.ListCreateAPIView):
    """
    API view for listing all book reviews and creating
    new one with admin permission.
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        # Ensure that the creation logic is not duplicated      
        instance = serializer.save(user=self.request.user)


class ReviewGetApiView(UserQuerySetMixin, generics.RetrieveAPIView):
    """
    API view for retrieving details of a book review with user-specific queryset.
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewDetailSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'pk'


class ReviewUpdateApiView(UserQuerySetMixin, generics.RetrieveUpdateAPIView):
    """
    API view for updating details of a book review with user-specific queryset.
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_update(self, serializer):
        # Extract the user from the updated data
        updated_user = serializer.validated_data.get('user')

        # If the user is not an admin and is trying to reassign the review, raise an error
        if not self.request.user.is_staff and updated_user != self.request.user:
            raise PermissionDenied(
                "You are not allowed to reassign the review to another user.")

        # Continue with the update and save the instance
        instance = serializer.save()


class ReviewDeleteApiView(generics.RetrieveDestroyAPIView):
    """
    API view for deleting a book review with admin permission
    and Bearer Token authentication.
    """
    queryset = BookReview.objects.all()
    serializer_class = BookReviewDetailSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


################## Order ####################
class OrderListApiView(generics.ListAPIView):
    """
    API view for retrieving a list of all orders and
    order items with admin user permission.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomAPIListPagination
    authentication_classes = [BearerTokenAuthentication]


class OrderGetDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    API view for retrieving and deleting the details of a specific order,
    including order items, with admin user permission.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomAPIListPagination
    authentication_classes = [BearerTokenAuthentication]
