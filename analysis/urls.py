from django.urls import path 
from .views import display_pivot_tables, index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', display_pivot_tables, name='display_pivot_tables'),
    path('', index, name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    