from django.contrib import admin
from django.urls import path, include
# import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("api_DRF.urls")),
    # path("__debug__/", include(debug_toolbar.urls)),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)