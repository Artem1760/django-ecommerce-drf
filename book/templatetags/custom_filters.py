from django import template

register = template.Library()

@register.filter(name='get_value')
def get_value(dictionary, key):
    """Star rate filter."""
    return dictionary.get(key, 0)


@register.filter(name='get_book_total_price')
def get_book_total_price(cart, book_id):
    """Filter to get the total price for a specific book in the cart."""
    return cart.get_book_total_price(book_id)


@register.filter(name='review_rating_percentage')
def review_rating_percentage(star_rating):
    """Star rating width percentage in the book_detail function for added reviews."""
    return int((star_rating / 5) * 80)


@register.filter(name='book_rating_percentage')
def book_rating_percentage(average_star_rating):
    """Star rating width percentage for all books."""
    star_width_percentage = (int(average_star_rating) / 5) * 80
    return int(star_width_percentage)
