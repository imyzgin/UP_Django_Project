from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user_status = UserBookStatus.objects.get(
                    user=self.request.user, 
                    book=self.object
                )
                context['user_status'] = user_status.status
                context['user_status_display'] = user_status.get_status_display()
            except UserBookStatus.DoesNotExist:
                context['user_status'] = None
                context['user_status_display'] = None
        return context
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
            
        self.object = self.get_object()
        status = request.POST.get('status')
        
        if status == 'remove':
            UserBookStatus.objects.filter(
                user=request.user, 
                book=self.object
            ).delete()
            messages.success(request, 'Книга удалена из ваших списков')
        else:
            user_status, created = UserBookStatus.objects.get_or_create(
                user=request.user,
                book=self.object,
                defaults={'status': status}
            )
            
            if not created:
                user_status.status = status
                user_status.save()
            
            messages.success(request, f'Статус книги обновлен на "{user_status.get_status_display()}"')
        
        return redirect('book_detail', pk=self.object.pk)

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

@login_required
def profile(request):
    reading_books = UserBookStatus.objects.filter(
        user=request.user, 
        status='reading'
    ).select_related('book')
    
    read_books = UserBookStatus.objects.filter(
        user=request.user, 
        status='read'
    ).select_related('book')
    
    dropped_books = UserBookStatus.objects.filter(
        user=request.user, 
        status='dropped'
    ).select_related('book')
    
    favorite_books = UserBookStatus.objects.filter(
        user=request.user, 
        status='favorite'
    ).select_related('book')
    
    want_to_read_books = UserBookStatus.objects.filter(
        user=request.user, 
        status='want_to_read'
    ).select_related('book')
    
    context = {
        'reading_books': reading_books,
        'read_books': read_books,
        'dropped_books': dropped_books,
        'favorite_books': favorite_books,
        'want_to_read_books': want_to_read_books,
    }
    
    return render(request, 'profile.html', context)