from django.contrib.auth import get_user_model
from rest_framework import serializers

from book.models import (Author, Book, BookLanguage, BookReview,
                         BookType, Category, FilterPrice, Publisher)
from checkout.models import Address, Order, OrderItem
from .validators import (validate_discount_price, validate_num_zero,
                         validate_text_len, validate_sale_and_discount,
                         validate_required_field,
                         unique_author_name, unique_book_title,
                         unique_category_name, unique_book_type,
                         unique_publisher_name, unique_language)
from .mixins import RelatedURLsMixin


############### User ##############
class UserAddressInLineSerializer(serializers.ModelSerializer):
    """Nested serializer with address data"""

    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'postcode',
                  'country', 'street_address', 'town_city', 'country_state',
                  'delivery_instructions', 'default']


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer for user detail data available only for admin user"""
    addresses = UserAddressInLineSerializer(read_only=True, many=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'email',
                  'phone', 'is_active', 'is_staff', 'is_superuser',
                  'addresses']


class UserPublicSerializer(serializers.Serializer):
    """Serializer for exposing public user data."""
    username = serializers.CharField(read_only=True)
    endpoint = serializers.HyperlinkedIdentityField(view_name='api:user',
                                                    lookup_field='pk',
                                                    read_only=True)


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for listing users and creating new users."""
    endpoint = serializers.HyperlinkedIdentityField(view_name='api:user',
                                                    lookup_field='pk',
                                                    read_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'endpoint']

    ################# Book ##################


class BookReviewSerializer(serializers.ModelSerializer):
    """Serializer for listing and creating reviews."""
    owner = UserPublicSerializer(source='user', read_only=True)
    id = serializers.IntegerField(read_only=True)
    review = serializers.CharField(validators=[validate_text_len])
    get_review_url = serializers.HyperlinkedIdentityField(
        view_name='api:review-detail', lookup_field='pk')

    class Meta:
        model = BookReview
        fields = ['get_review_url', 'id', 'star_rating', 'review', 'book',
                  'owner']


class BookReviewDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for BookReview model."""
    owner = UserPublicSerializer(source='user', read_only=True)
    id = serializers.IntegerField(read_only=True)
    review = serializers.CharField(validators=[validate_text_len])
    update_url = serializers.HyperlinkedIdentityField(
        view_name='api:review-update', lookup_field='pk')
    delete_url = serializers.HyperlinkedIdentityField(
        view_name='api:review-delete', lookup_field='pk')
    book = serializers.CharField(read_only=True)

    class Meta:
        model = BookReview
        fields = ['id', 'owner', 'star_rating', 'review', 'book', 'update_url',
                  'delete_url']


class BookLanguageSerializer(serializers.ModelSerializer):
    get_language_url = serializers.HyperlinkedIdentityField(
        view_name='api:language', lookup_field='pk')
    language = serializers.CharField(
        validators=[unique_language, validate_text_len])

    class Meta:
        model = BookLanguage
        fields = ['id', 'language', 'get_language_url']


class CategorySerializer(serializers.ModelSerializer):
    get_category_url = serializers.HyperlinkedIdentityField(
        view_name='api:category', lookup_field='pk')
    name = serializers.CharField(
        validators=[unique_category_name, validate_text_len])
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'is_active', 'get_category_url']


class BookTypeSerializer(serializers.ModelSerializer):
    get_type_url = serializers.HyperlinkedIdentityField(
        view_name='api:book-type', lookup_field='pk')
    name = serializers.CharField(
        validators=[unique_book_type, validate_text_len])

    class Meta:
        model = BookType
        fields = ['id', 'name', 'get_type_url']


class PublisherSerializer(serializers.ModelSerializer):
    get_publisher_url = serializers.HyperlinkedIdentityField(
        view_name='api:publisher', lookup_field='pk')
    name = serializers.CharField(
        validators=[unique_publisher_name, validate_text_len])

    class Meta:
        model = Publisher
        fields = ['id', 'name', 'get_publisher_url']


class AuthorSerializer(serializers.ModelSerializer):
    get_author_url = serializers.HyperlinkedIdentityField(
        view_name='api:author', lookup_field='pk')
    name = serializers.CharField(
        validators=[unique_author_name, validate_text_len])
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'slug', 'get_author_url']


class BookSerializer(serializers.ModelSerializer):
    """Serializer for listing and books"""
    # HyperlinkedIdentityField to get, update, delete the book
    get_book_url = serializers.HyperlinkedIdentityField(view_name='api:book',
                                                        lookup_field='pk',
                                                        read_only=True)

    # Read-only during creation
    slug = serializers.CharField(read_only=True)

    # Other fields with validators and required conditions    
    title = serializers.CharField(
        validators=[unique_book_title, validate_text_len])
    quantity = serializers.IntegerField(validators=[validate_num_zero],
                                        required=True)
    regular_price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                             validators=[validate_num_zero],
                                             required=True)
    num_pages = serializers.IntegerField(validators=[validate_num_zero],
                                         required=True)
    publisher = serializers.CharField(validators=[validate_text_len],
                                      required=True)
    author = serializers.CharField(validators=[validate_text_len],
                                   required=True)
    category = serializers.CharField(validators=[validate_text_len],
                                     required=True)
    publication_date = serializers.CharField(required=True)

    # SlugRelatedFields for related objects
    book_type = serializers.SlugRelatedField(many=True,
                                             queryset=BookType.objects.all(),
                                             slug_field='name', required=True)
    languages = serializers.SlugRelatedField(many=True,
                                             queryset=BookLanguage.objects.all(),
                                             slug_field='language',
                                             required=True)
    filter_price = serializers.SlugRelatedField(
        queryset=FilterPrice.objects.all(), slug_field='price', required=True)

    # SerializerMethodFields for computed fields
    sale_percentage = serializers.SerializerMethodField(read_only=True)
    average_star_rating = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'get_book_url', 'title', 'slug', 'isbn',
                  'publication_date', 'regular_price', 'discount_price', 
                  'is_sale', 'sale_percentage', 'cover', 'average_star_rating', 
                  'description', 'specification', 'quantity', 'created_date', 
                  'is_active', 'num_pages', 'category', 'author', 'book_type', 
                  'publisher', 'languages', 'filter_price']

    def get_sale_percentage(self, obj):
        return obj.get_percentage()

    def get_average_star_rating(self, obj):
        return obj.average_star_rating()

    def validate(self, data):
        # Additional validation logic using custom validators
        validate_sale_and_discount(data),
        validate_discount_price(data)
        validate_required_field(data['languages'], "Languages")
        validate_required_field(data['book_type'], "Book Type")
        return data

    def create(self, validated_data):
        # Extract data for related objects (publisher, author, category)           
        publisher_data = validated_data.pop('publisher', None)
        author_data = validated_data.pop('author', None)
        category_data = validated_data.pop('category', None)

        # Get or create instances for related objects
        publisher_instance, _ = Publisher.objects.get_or_create(
            name=publisher_data)
        author_instance, _ = Author.objects.get_or_create(name=author_data)
        category_instance, _ = Category.objects.get_or_create(
            name=category_data)

        # Assign related objects to the validated data
        validated_data['publisher'] = publisher_instance
        validated_data['author'] = author_instance
        validated_data['category'] = category_instance

        return super().create(validated_data)


class BookDetailSerializer(RelatedURLsMixin, serializers.ModelSerializer):
    """
    Serializer for detailed book data including related reviews and hyperlinked URLs.
    """
    # Nested serializer for related reviews
    reviews = BookReviewSerializer(many=True, read_only=True)

    # Read-only during creation
    slug = serializers.CharField(read_only=True)

    # Fields with custom validators and required conditions
    title = serializers.CharField(validators=[unique_book_title])
    publication_date = serializers.CharField(required=True)
    quantity = serializers.IntegerField(validators=[validate_num_zero],
                                        required=True)
    regular_price = serializers.DecimalField(max_digits=10, decimal_places=2,
                                             validators=[validate_num_zero],
                                             required=True)
    num_pages = serializers.IntegerField(validators=[validate_num_zero],
                                         required=True)
    publisher = serializers.CharField(validators=[validate_text_len],
                                      required=True)
    author = serializers.CharField(validators=[validate_text_len],
                                   required=True)
    category = serializers.CharField(validators=[validate_text_len],
                                     required=True)

    # SlugRelatedFields for related objects
    book_type = serializers.SlugRelatedField(many=True,
                                             queryset=BookType.objects.all(),
                                             slug_field='name', required=True)
    languages = serializers.SlugRelatedField(many=True,
                                             queryset=BookLanguage.objects.all(),
                                             slug_field='language',
                                             required=True)
    filter_price = serializers.SlugRelatedField(
        queryset=FilterPrice.objects.all(), slug_field='price', required=True)

    # SerializerMethodFields for hyperlinked URLs of related objects
    publisher_url = serializers.SerializerMethodField(read_only=True)
    author_url = serializers.SerializerMethodField(read_only=True)
    book_type_url = serializers.SerializerMethodField(read_only=True)
    languages_url = serializers.SerializerMethodField(read_only=True)
    category_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'slug', 'isbn', 'publication_date',
                  'regular_price', 'discount_price', 'is_sale', 'cover',
                  'description', 'specification', 'quantity', 'created_date',
                  'is_active', 'num_pages', 'category', 'author', 'book_type',
                  'publisher', 'languages', 'filter_price', 'reviews',
                  'publisher_url', 'author_url', 'book_type_url', 'languages_url',
                  'category_url']

    def update(self, instance, validated_data):
        # Extract data for related objects (publisher, author, category)
        publisher_data = validated_data.pop('publisher', None)
        author_data = validated_data.pop('author', None)
        category_data = validated_data.pop('category', None)

        # Get or create instances for related objects
        publisher_instance, _ = Publisher.objects.get_or_create(
            name=publisher_data)
        author_instance, _ = Author.objects.get_or_create(name=author_data)
        category_instance, _ = Category.objects.get_or_create(
            name=category_data)

        # Update or create related objects
        instance.publisher = publisher_instance
        instance.author = author_instance
        instance.category = category_instance

        return super().update(instance, validated_data)

    def validate(self, data):
        # Additional validation logic using custom validators
        validate_sale_and_discount(data)
        validate_discount_price(data)
        validate_required_field(data['languages'], "Languages")
        validate_required_field(data['book_type'], "Book Type")
        return data


class BookInLineSerializer(serializers.ModelSerializer):
    """
    Nested serializer for minimal book data to be used in related representations.
    """
    author = serializers.CharField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'num_pages']

    ############### Order ##############


class OrderItemInLineSerializer(serializers.ModelSerializer):
    """Nested serializer for order items to be used in related representations."""
    # Include BookInLineSerializer for detailed information about the ordered book
    book = BookInLineSerializer()
    language = serializers.CharField()
    book_type = serializers.CharField()
    # 'item_number' is a calculated field representing the position of
    # the order item in the order
    item_number = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_number', 'book', 'quantity', 'price',
                  'subtotal_price', 'language', 'book_type']

    def get_item_number(self, instance):
        """
        Calculate and return the position of the order item in the order's item list.
        """
        return instance.order.items.all().order_by('id').values_list('id',
                             flat=True).filter(id__lte=instance.id).count()


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for representing order data."""
    customer = UserPublicSerializer(source='user', read_only=True)
    delivery = serializers.StringRelatedField()
    created_date = serializers.DateTimeField()
    get_order_url = serializers.HyperlinkedIdentityField(view_name='api:order',
                                                         lookup_field='pk',
                                                         read_only=True)

    class Meta:
        model = Order
        exclude = ['shipping_address']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serializer for representing detailed order data, 
    including information about shipping address and order items."""
    delivery = serializers.StringRelatedField()
    created_date = serializers.DateTimeField()
    customer = UserPublicSerializer(source='user', read_only=True)
    shipping_address = UserAddressInLineSerializer(read_only=True)
    order_items = OrderItemInLineSerializer(read_only=True, many=True,
                                            source='items')  # 'items' is OrderItems model

    class Meta:
        model = Order
        fields = ['customer', 'oid', 'total_price', 'delivery',
                  'transaction_id', 'payment_option', 'order_status',
                  'created_date', 'shipping_address', 'order_items']

    def get_shipping_address(self, obj):
        default_address = obj.user.addresses.filter(default=True).first()
        if default_address:
            return UserAddressInLineSerializer(default_address).data
        return None
