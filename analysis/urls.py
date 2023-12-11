from django.urls import path 
from .views import display_pivot_tables, index

urlpatterns = [
    path('', display_pivot_tables, name='display_pivot_tables'),
    path('', index, name='index')
]