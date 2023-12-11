from django.urls import path 
from .views import display_pivot_tables, index, display_sales_analysis

urlpatterns = [
    path('', display_pivot_tables, name='display_pivot_tables'),
    path('', index, name='index'),
    path('sales-analysis/', display_sales_analysis, name='sales_analysis'),
]