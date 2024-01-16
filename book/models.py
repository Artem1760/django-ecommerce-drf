from ckeditor.fields import RichTextField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, Q
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager

CustomerUser = settings.AUTH_USER_MODEL

RATING = (
    (1, '★☆☆☆☆'),
    (2, '★★☆☆☆'),
    (3, '★★★☆☆'),
    (4, '★★★★☆'),
    (5, '★★★★★'),
)

FILTER_PRICE = (
    ('Under $25', 'Under $25'),
    ('$25 to $50', '$25 to $50'),
    ('$50 to $100', '$50 to $100'),
    ('$100 to $200', '$100 to $200'),
    ('$200 & Above', '$200 & Above'),
)


class Category(models.Model):
    name = models.CharField(unique=True, max_length=100, db_index=True)
    slug = models.SlugField(max_length=200)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book:category', kwargs={'slug': self.slug})

    def get_book_count(self):
        return Book.objects.filter(category=self, is_active=True).count()

    def save(self, *args, **kwargs):
        # Update the slug field based on the name field
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BookType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _('Book type')
        verbose_name_plural = _('Book types')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = ShortUUIDField(primary_key=True, unique=True, length=10,
                        max_length=12, editable=False, alphabet='1234567890')
    title = models.CharField(max_length=200, db_index=True,
                             unique=True)  # db_index=True is for better searching
    slug = models.SlugField()
    publication_date = models.DateField()
    isbn = ShortUUIDField(unique=True, length=13, max_length=25, prefix='isbn',
                          editable=False, alphabet='1234567890')
    regular_price = models.DecimalField(verbose_name=_('Regular price'),
                                        max_digits=10, decimal_places=2,
                                        default=10)
    discount_price = models.DecimalField(verbose_name=_('Discount price'),
                                         max_digits=10, decimal_places=2,
                                         default=0, null=True, blank=True)
    is_sale = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='book_covers',
                              default='book_default.png', null=True,
                              blank=True)
    description = RichTextField(null=True, blank=True,
                                default='This is the book', db_index=True)
    specification = RichTextField(null=True, blank=True,
                                  default='Book Specification')
    quantity = models.IntegerField(default='25', null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, editable=False)
    is_active = models.BooleanField(default=True)
    num_pages = models.PositiveIntegerField(null=True, blank=True)
    tags = TaggableManager(blank=True)
    users_wishlist = models.ManyToManyField(CustomerUser,
                                            related_name='users_wishlist',
                                            blank=True)

    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 related_name='category', null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE,
                               related_name='author')
    book_type = models.ManyToManyField('BookType', related_name='types')
    publisher = models.ForeignKey('Publisher', on_delete=models.SET_NULL,
                                  related_name='publisher', null=True)
    languages = models.ManyToManyField('BookLanguage',
                                       related_name='languages')
    filter_price = models.ForeignKey('FilterPrice', on_delete=models.SET_NULL,
                                     null=True, blank=True)

    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ('-created_date', 'title')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book:book-detail', kwargs={'slug': self.slug})

    def get_percentage(self):
        """Get discount percentage"""
        if self.is_sale:
            discount_percentage = (
                (self.regular_price - self.discount_price) / self.regular_price) * 100
            return round(discount_percentage, 0)
        return 0

    def average_star_rating(self):
        """Average rating for a specific book"""
        avg_rating = self.reviews.aggregate(avg_rating=Avg('star_rating'))[
                         'avg_rating'] or 0
        return round(avg_rating, 1)

    def book_search(query):
        # Split the search query into words
        search_words = query.split()
        # Prepare the Q objects for searching
        search_filters = Q()
        for word in search_words:
            search_filters |= (
                    Q(title__icontains=word) |
                    Q(description__icontains=word) |
                    Q(author__name__icontains=word) |
                    Q(category__name__icontains=word) |
                    Q(publisher__name__icontains=word)
            )
        # Perform the search query
        search_results = Book.objects.filter(search_filters).distinct()
        return search_results

    def clean(self):
        """Prices checks"""
        # Call the parent clean method to ensure all default validations are performed
        super().clean()

        # Check if discount_price is not None and is_sale is False
        if self.discount_price is not None and not self.is_sale:
            raise ValidationError({
                'is_sale': 'If discount_price is not None, is_sale must be True.'})

        # Check if is_sale is True and discount_price is None
        if self.is_sale and self.discount_price is None:
            raise ValidationError({
                'discount_price': 'If is_sale is True, discount_price cannot be None.'})

        # Check if discount_price is lower than regular_price
        if self.discount_price is not None and self.discount_price >= self.regular_price:
            raise ValidationError({
                'discount_price': 'Discount price must be lower than regular price.'})

    def save(self, *args, **kwargs):
        # Update the slug field based on the name field
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BookImage(models.Model):
    """
    Book Image table.
    """
    book = models.ForeignKey('Book', on_delete=models.CASCADE,
                             related_name='book_images')
    image = models.ImageField(upload_to='book_images',
                              default='default_avatar.png', null=True,
                              blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Book image')
        verbose_name_plural = _('Book images')

    def get_absolute_url(self):
        """Displays images on website"""
        return reverse('book:book-detail', args=[self.pk])


class BookLanguage(models.Model):
    language = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = _('Book language')
        verbose_name_plural = _('Book languages')

    def __str__(self):
        return self.language


class Publisher(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True)

    class Meta:
        verbose_name = _('Publisher')
        verbose_name_plural = _('Publishers')
        ordering = ('name',)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150)

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_book_count(self):
        return Book.objects.filter(author=self, is_active=True).count()

    def get_absolute_url(self):
        return reverse('book:authors', args=[self.slug])

    def save(self, *args, **kwargs):
        # Update the slug field based on the name field
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class BookReview(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE,
                             related_name='reviews')
    user = models.ForeignKey(CustomerUser, on_delete=models.CASCADE)
    star_rating = models.PositiveIntegerField(choices=RATING)
    review = models.CharField(max_length=255)
    created_date = models.DateField(auto_now_add=True, editable=False)
    updated_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name = _('Book Review')
        verbose_name_plural = _('Book Reviews')

    def __str__(self):
        return self.review

    def clean(self):
        if self.star_rating is None or self.star_rating == 0:
            raise ValidationError(
                {'star_rating': 'Please select a valid star rating.'})


class FilterPrice(models.Model):
    """Book price rangers"""
    price = models.CharField(max_length=100, choices=FILTER_PRICE)

    def __str__(self):
        return self.price
