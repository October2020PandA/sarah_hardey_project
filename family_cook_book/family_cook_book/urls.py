from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from recipe_app.models import Recipe 

urlpatterns = [
    path('', include('recipe_app.urls')),
    path('admin/',admin.site.urls),
    path('recipe_app/', include('recipe_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) ## debug for images
    import debug_toolbar ## debug toolbar - remove before publishing
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns