from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Avg, Func, IntegerField, Count, Q, Case, When, F, \
    ExpressionWrapper, DecimalField
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from taggit.models import Tag

from .forms import BookReviewForm
from .models import BookReview, Category, Book, Author, FilterPrice, RATING


############# To be used in the different views ##############
def paginate_books(request, books, items_per_page=4):
    """Helper function to paginate a queryset"""
    page_number = request.GET.get('page', 1)
    paginator = Paginator(books, items_per_page)

    try:
        paginated_books = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_books = paginator.page(1)
    except EmptyPage:
        paginated_books = paginator.page(paginator.num_pages)

    # The sortby parameter to the pagination links
    sortby_param = request.GET.get('sortby', '')
    paginated_books.sortby_param = sortby_param

    return paginated_books


def sort_books(request, book_qs):
    """
    Helper function for sorting books by review, rating, price and by date.
    Used in functions: authors, tags, hot_offers, search_view, related_books, 
    """
    sort_option = request.GET.get('sortby')

    match sort_option:
        case 'most-reviewed':
            return book_qs.annotate(num_reviews=Count('reviews')).order_by(
                '-num_reviews')
        case 'most-rated':
            return book_qs.annotate(
                avg_rating=Avg('reviews__star_rating')).order_by('-avg_rating')
        case 'price-LH':
            return book_qs.annotate(
                sorted_price=Case(
                    When(is_sale=True, then=F('discount_price')),
                    When(is_sale=False, then=F('regular_price'))
                )).order_by('sorted_price')
        case 'price-HL':
            return book_qs.annotate(
                sorted_price=Case(
                    When(is_sale=True, then=F('discount_price')),
                    When(is_sale=False, then=F('regular_price'))
                )).order_by('-sorted_price')
        case 'old':
            return book_qs.order_by('created_date')
        case _:
            return book_qs


######################## Category ########################
def category_list(request):
    """List of all categories"""
    books = Book.objects.filter(is_active=True)[:4]
    categories_with_books = Category.objects.annotate(
        book_count=Count('category')).filter(book_count__gt=0)
    context = {
        'categories_with_books': categories_with_books,
        'books': books,
        'title': 'Categories',
    }
    return render(request, 'book/category_list.html', context)


def category_book_list(request, slug):
    """List of books displayed to the selected category"""
    category = get_object_or_404(Category, is_active=True, slug=slug)
    books = Book.objects.filter(is_active=True, category=category)

    sorted_books = sort_books(request, books)
    # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = books

    paginated_books = paginate_books(request, books_to_display)

    context = {
        'books': paginated_books,
        'title': f'Category | {category}',
        'obj': category,
        'category_product_list': 'Used as a key for the header distinction',
        'total_books_count': books.count(),
        # Pagination
        'is_paginated': paginated_books.has_other_pages,
    }
    return render(request, 'book/generic_product_list.html', context)


############# Product list filter components #############
def get_selected_filter(request):
    """Helper function to get selected filter parameters from the request"""
    return {
        'category': request.GET.get('category'),
        'filter-price': request.GET.get('filter-price'),
        'author': request.GET.get('author'),
        'tag': request.GET.get('tag'),
        'rating': int(request.GET.get('rating', 0)),
    }


def get_books_with_filter(books, selected_filter, filter_field):
    """Helper function to filter books based on selected filter."""
    if selected_filter:
        return books.filter(is_active=True, **{filter_field: selected_filter})
    return books.filter(is_active=True)


def get_books_with_rating_filter(books, selected_rating_id):
    """Helper function to filter books based on rating."""
    if selected_rating_id:
        lower_range = selected_rating_id
        upper_range = selected_rating_id + 0.9
        return books.annotate(avg_rating=Avg('reviews__star_rating')).filter(
            avg_rating__range=(lower_range, upper_range))
    return books


def get_rating_counts(books, ratings):
    """
    Helper function to calculate rating counts for a list of books
    and given ratings.

    Args:
    - books: QuerySet of Book objects.
    - ratings: List of rating values.

    Returns:
    - rating_counts: Dictionary where keys are ratings and values are
      the corresponding counts.
    """
    rating_counts = {}
    for rating in ratings:
        # Use Django's Func to round the average star rating to the nearest integer
        rounded_avg = Func(Avg('reviews__star_rating'), function='FLOOR',
                           output_field=IntegerField())
        # Annotate the books with the rounded average and filter by the current rating
        filtered_books = books.annotate(rounded_avg=rounded_avg).filter(
            rounded_avg=rating).distinct()
        # Count the number of books for the current rating and store in the dictionary
        rating_counts[rating] = filtered_books.count()
    return rating_counts


def book_list_filter(request):
    """
    Display all books, selected books to the price, rating, category, tags, author
    """
    authors = Author.objects.all()
    tags = Tag.objects.all()
    filter_price = FilterPrice.objects.all()
    books = Book.objects.filter(is_active=True)

    ratings = [5, 4, 3, 2, 1]
    rating_widths = {rating: rating * 20 for rating in ratings}
    rating_counts = get_rating_counts(books, ratings)

    selected_filter = get_selected_filter(request)

    # Filter books based on selected criteria
    books = get_books_with_filter(books, selected_filter['category'],
                                  'category')
    books = get_books_with_filter(books, selected_filter['filter-price'],
                                  'filter_price')
    books = get_books_with_filter(books, selected_filter['author'], 'author')
    books = get_books_with_filter(books, selected_filter['tag'], 'tags')
    books = get_books_with_rating_filter(books, selected_filter['rating'])

    # Paginate the filtered books using the helper function
    paginated_books = paginate_books(request, books)

    context = {
        'books': paginated_books,
        'tags': tags,
        'authors': authors,
        'title': 'Books',
        'rating_counts': rating_counts,
        'selected_rating': selected_filter['rating'],
        'rating_widths': rating_widths,
        'filter_price': filter_price,
        'total_books_count': books.count(),
        # Title of the selected filter:
        'selected_price': get_object_or_404(FilterPrice, id=selected_filter[
            'filter-price']) if selected_filter['filter-price'] else None,
        'selected_author': get_object_or_404(Author,
                                             id=selected_filter['author']) if
        selected_filter['author'] else None,
        'selected_category': get_object_or_404(Category, id=selected_filter[
            'category']) if selected_filter['category'] else None,
        'selected_tag': get_object_or_404(Tag, id=selected_filter['tag']) if
        selected_filter['tag'] else None,
        'selected_filter': selected_filter,
        # Pagination               
        'is_paginated': paginated_books.has_other_pages,
    }

    return render(request, 'book/product_list_filter.html', context)


############## Book detail components ##############
def related_books(request, slug):
    """List of all related books used in the book_detail()"""
    book = get_object_or_404(Book, slug=slug, is_active=True)
    related_books = Book.objects.filter(
        Q(category=book.category) | Q(author=book.author))

    sorted_books = sort_books(request, related_books)
    # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = related_books

        # Paginate the filtered books using the helper function
    paginated_books = paginate_books(request, books_to_display)
    context = {
        'book': book,
        'books': paginated_books,
        'total_books_count': related_books.count(),
        'related_books': 'Used as a key for the header distinction',
        'title': f'Related Books to {book}',
        'obj': 'More Related Books For You:',
        # Pagination      
        'is_paginated': paginated_books.has_other_pages,
    }

    return render(request, 'book/generic_product_list.html', context)


def recently_viewed(request, slug):
    """
    Helper function for the list of recently viewed books used in the book_detail().
    """
    recently_viewed_books = None
    if 'recently_viewed' in request.session:
        # Remove the current book's slug if already present
        if slug in request.session['recently_viewed']:
            request.session['recently_viewed'].remove(slug)

        # Filter books based on slugs in 'recently_viewed' and sort by the order in the session
        recently_viewed = Book.objects.filter(
            slug__in=request.session['recently_viewed'])
        recently_viewed_books = sorted(recently_viewed,
                                       key=lambda x: request.session[
                                           'recently_viewed'].index(x.slug))

        # Insert the current book's slug at the beginning of the list
        request.session['recently_viewed'].insert(0, slug)

        # Limit the list to the last 7 viewed books
        if len(request.session['recently_viewed']) > 7:
            request.session['recently_viewed'].pop()
    else:
        # If 'recently_viewed' is not present in the session, initialize it
        # with the current book's slug
        request.session['recently_viewed'] = [slug]

    request.session.modified = True
    return recently_viewed_books


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, is_active=True)
    related_books = Book.objects.filter(category=book.category).exclude(
        slug=book.slug)[:4]
    author = Author.objects.filter(slug=slug)
    review_form = BookReviewForm()

    recently_viewed_books = recently_viewed(request, slug)

    context = {
        'book': book,
        'related_books': related_books,
        'author': author,
        'title': f'Book | {book}',
        'review_form': review_form,
        'RATING': RATING,
        'recently_viewed_books': recently_viewed_books,
    }
    return render(request, 'book/product_detail.html', context)


@login_required(login_url='account:login')
def add_review(request, slug):
    """Create a review for the book related to the book_detail()"""
    book = get_object_or_404(Book, slug=slug, is_active=True)
    if request.method == 'POST':
        review_form = BookReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review added successfully.')

            return redirect('book:book-detail', slug=book.slug)

        messages.error(request,
                       'There was an error in the form submission. '
                       'All fields have to be filled in.')
    else:
        # If it's a GET request, create a new instance of the review form
        review_form = BookReviewForm()

    return render(request, 'book/partials/add_review.html',
                  {'review_form': review_form})


@login_required(login_url='account:login')
def update_review(request, pk):
    """Edit a review related to the book_detail()"""
    feedback = BookReview.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        # Form will be prefilled with the existing review data
        review_form = BookReviewForm(instance=feedback, data=request.POST)

        if review_form.is_valid():
            review_form.save(commit=False)
            review_form.star_rating = request.POST.get('star_rating')
            review_form.review = request.POST.get('review')
            review_form.save()
            messages.success(request, 'Review was updated successfully.')
            return redirect('book:book-detail', slug=feedback.book.slug)
    else:
        # If it's a GET request, create a new instance of the review form
        # with the existing review data
        review_form = BookReviewForm(instance=feedback)

    context = {
        'review_form': review_form,
        'feedback': feedback,
        'RATING': RATING,
        'title': 'Edit Review',
    }
    return render(request, 'book/update_review.html', context)


@login_required(login_url='account:login')
def delete_review(request, pk):
    """Delete review related to the book_detail()"""
    review = BookReview.objects.get(id=pk)
    if request.user != review.user:
        return HttpResponse('You can not delete it!')

    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review was deleted successfully.')
        return redirect('book:book-detail', slug=review.book.slug)
    return render(request, 'book/review_delete.html',
                  {'review': review, 'title': 'Sign Up'}
                  )


##################### Search #####################
def search_view(request):
    """List of books based on the search"""
    query = request.GET.get('q')

    if query:
        search_results = Book.book_search(query)
        sorted_books = sort_books(request, search_results)
    else:
        # Empty queryset if no query provided
        search_results = Book.objects.none()
        sorted_books = sort_books(request, search_results)

        # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = search_results

    paginated_books = paginate_books(request, books_to_display)

    context = {
        'books': paginated_books,
        'obj': f'Search Results for "{query}"',
        'title': 'Search Result',
        'total_books_count': search_results.count(),
        # Pagination               
        'is_paginated': paginated_books.has_other_pages,
        'search': 'key for paginator page & generic header distinction'
    }

    return render(request, 'book/generic_product_list.html', context)


################ Other book lists ################
def hot_offers(request):
    """
    View to display a list of books on sale, considering discounts
    and sorting options.
    """
    books = Book.objects.filter(is_active=True, is_sale=True)
    # Annotate books with the discount percentage and order by it
    books = books.annotate(discount_percentage=ExpressionWrapper(
        F('discount_price') / F('regular_price') * 100,
        output_field=DecimalField()
    )).order_by('discount_percentage')

    # Sort the books based on user preferences
    sorted_books = sort_books(request, books)

    # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = books

        # Paginate the books for display
    paginated_books = paginate_books(request, books_to_display)
    context = {
        'books': paginated_books,
        'title': 'Hot Offers',
        'obj': 'Hot Offers',
        'total_books_count': len(sorted_books),
        # Pagination               
        'is_paginated': paginated_books.has_other_pages,
    }

    return render(request, 'book/generic_product_list.html', context)


def tag_list(request):
    """Display all list of available tags"""
    tags = Tag.objects.all()
    books = Book.objects.filter(is_active=True)[:4]
    context = {
        'tags': tags,
        'books': books,
        'title': 'Tags',
    }
    return render(request, 'book/author_tag_list.html', context)


def tags(request, slug=None):
    """View to display a list of books based on the selected tag."""
    books = Book.objects.filter(is_active=True)

    tag = None
    if slug:
        tag = get_object_or_404(Tag, slug=slug)
        # Filter books based on the selected tag
        books = books.filter(tags__in=[tag])

    sorted_books = sort_books(request, books)
    # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = books

        # Paginate the books for display
    paginated_books = paginate_books(request, books_to_display)

    context = {
        'books': paginated_books,
        'total_books_count': books.count(),
        'obj': f'Filtered by Tag: #{tag.name}',
        'title': f'Books|#{tag}',
        # Pagination               
        'is_paginated': paginated_books.has_other_pages,
    }

    return render(request, 'book/generic_product_list.html', context)


def author_list(request):
    """Display a list of available authors"""
    authors = Author.objects.filter(author__is_active=True).distinct()
    books = Book.objects.filter(is_active=True)[:4]

    context = {
        'authors': authors,
        'books': books,
        'title': 'Authors',
    }

    return render(request, 'book/author_tag_list.html', context)


def authors(request, slug):
    """View to display a list of books based on the selected author."""
    author = get_object_or_404(Author, slug=slug)
    # Get all active books by the selected author and order by created date
    books = Book.objects.filter(is_active=True, author=author).order_by(
        '-created_date')

    # Sort the books based on user preferences
    sorted_books = sort_books(request, books)

    # Check if sorted books are selected, use them, otherwise use the original books
    if sorted_books.exists():
        books_to_display = sorted_books
    else:
        books_to_display = books

    # Paginate the books for display    
    paginated_books = paginate_books(request, books_to_display)

    context = {
        'obj': f'Books by "{author}"',
        'books': paginated_books,
        'title': f'Books|By {author}',
        'total_books_count': books.count(),
        # Pagination               
        'is_paginated': paginated_books.has_other_pages,
    }

    return render(request, 'book/generic_product_list.html', context)
