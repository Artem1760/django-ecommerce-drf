from book.models import Category


def default(request):
    categories = Category.objects.filter(is_active=True)

    context = {
        'categories': categories,
    }
    return context
