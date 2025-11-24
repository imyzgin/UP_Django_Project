from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.render_main, name='index'),
    path("books/<int:pk>", views.BookDetail.as_view(), name="book_detail"),
    path('catalog/', views.catalog, name='catalog'),
    path('books/<int:pk>/read/', views.read_book, name='read_book'),
    path('books/<int:book_pk>/read/chapter/<int:chapter_number>/', views.read_chapter, name='read_chapter'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('profile/', views.profile, name='profile'),
]