from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.views.generic import ListView, DetailView

from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404


def render_main(request): 
    popular_books = Book.objects.filter(id__in=[1, 3])
    
    new_books = Book.objects.filter(id__in=[2])
    
    data = {
        'popular_books': popular_books,  
        'new_books': new_books,          
        'authors': Author.objects.all(),
        'genres': Genre.objects.all(),
    }
    
    return render(request, 'index.html', data)

class BookDetail(DetailView):
   model = Book
   template_name = 'book_detail.html'
   context_object_name = "book"

def catalog(request):
    genres = Genre.objects.all()
    selected_genre_ids = request.GET.getlist('genre')
    search_query = request.GET.get('search', '')
    
    books = Book.objects.all()
    
    if search_query:
        books = books.filter(
            Q(bookName__icontains=search_query) |
            Q(author__firstName__icontains=search_query) |
            Q(author__lastName__icontains=search_query)
        ).distinct()
    
    if selected_genre_ids:
        for genre_id in selected_genre_ids:
            books = books.filter(genre__id=genre_id)
    
    return render(request, 'catalog.html', {
        'genres': genres, 
        'books': books,
        'selected_genre_ids': [int(id) for id in selected_genre_ids],
        'search_query': search_query
    })

def read_book(request, pk):
    book = Book.objects.get(id=pk)
    
    data = {
        'book': book,
    }
    
    return render(request, 'read_book.html', data)

def read_chapter(request, book_pk, chapter_number):
    book = get_object_or_404(Book, pk=book_pk)
    chapter = get_object_or_404(Chapter, book=book, chapter_number=chapter_number)
    
    previous_chapter = Chapter.objects.filter(
        book=book, 
        chapter_number__lt=chapter_number
    ).order_by('-chapter_number').first()
    
    next_chapter = Chapter.objects.filter(
        book=book, 
        chapter_number__gt=chapter_number
    ).order_by('chapter_number').first()
    
    all_chapters = Chapter.objects.filter(book=book).order_by('chapter_number')
    
    context = {
        'book': book,
        'chapter': chapter,
        'previous_chapter': previous_chapter,
        'next_chapter': next_chapter,
        'all_chapters': all_chapters,
        'current_chapter_number': chapter_number,
    }
    
    return render(request, 'read_chapter.html', context)