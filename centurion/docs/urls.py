from django.urls import path
from .views import generic_html_page_view

urlpatterns = [
    path('page/<path:page_name>', generic_html_page_view, name='doc_page_view'),
]