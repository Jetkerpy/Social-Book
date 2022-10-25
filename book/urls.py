from django.urls import path
from .views import (
    book_detail_view,
    star_rating_view,
    add_book,
)


app_name = 'book'

urlpatterns = [
    path('<int:pk>/', book_detail_view, name = 'detail'),
    path('rating', star_rating_view, name = 'rating'),
    path('add-book/', add_book, name = 'add-book'),
    

]