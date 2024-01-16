from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    # Local apps
    path('', include('core.urls', namespace='core')),
    path('account/', include('account.urls', namespace='account')),
    path('shop/', include('book.urls', namespace='book')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('checkout/', include('checkout.urls', namespace='checkout')),
    # Third party urls    
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # Rest Api
    path('api/', include('rest_api.urls', namespace='api')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # auth/token/login/

]

# handling the 404 error
handler404 = 'core.views.error_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
