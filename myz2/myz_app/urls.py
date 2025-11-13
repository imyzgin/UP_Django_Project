from django.urls import path
from . import views



urlpatterns = [
    path('', views.render_main, name ='index'),
    path("books/<int:pk>", views.BookDetail.as_view(), name = "book_detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('books/<int:pk>/read/', views.read_book, name='read_book'),
    
]