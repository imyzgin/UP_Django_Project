from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Author(models.Model):
    firstName = models.CharField(max_length=200)
    lastName = models.CharField(max_length=200)
    dateOfBirth = models.DateField()
    dateOfDeath = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.firstName + ' ' + self.lastName

class Book(models.Model):
    bookName = models.CharField(max_length=200)
    yearOfPublication = models.IntegerField()
    desc = models.TextField(max_length=512, blank=True, null=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    genre = models.ManyToManyField('Genre')
    publisher = models.ForeignKey('Publisher', on_delete=models.CASCADE)
    image = models.ImageField(upload_to="book_images/")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Цена")
    book_file = models.FileField(upload_to="book_files/", blank=True, null=True, verbose_name="Файл книги")

    def get_first_chapter(self):
        return self.chapters.first()
    
    def get_last_chapter(self):
        return self.chapters.last()

    def __str__(self):
        return self.bookName

class Chapter(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='chapters')
    chapter_number = models.PositiveIntegerField(verbose_name="Номер главы")
    title = models.CharField(max_length=200, verbose_name="Название главы")
    content = models.TextField(verbose_name="Текст главы")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['chapter_number']
        unique_together = ['book', 'chapter_number']
    
    def __str__(self):
        return f"{self.book.bookName} - Глава {self.chapter_number}: {self.title}"

class Genre(models.Model):
    genreName = models.CharField(max_length=200)
    def __str__(self):
        return self.genreName

class Review(models.Model):
    reviewText = models.TextField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    email = models.CharField(max_length=200)
    def __str__(self):
        return self.email

class Publisher(models.Model):
    publisher_name = models.CharField(max_length=200)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    def __str__(self):
        return self.publisher_name

class UserBookStatus(models.Model):
    STATUS_CHOICES = [
        ('read', 'Прочитано'),
        ('reading', 'Читаю'),
        ('dropped', 'Брошено'),
        ('favorite', 'Любимые'),
        ('want_to_read', 'Хочу прочитать'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'book'] 
        verbose_name_plural = "User book statuses"
    
    def __str__(self):
        return f"{self.user.username} - {self.book.bookName} ({self.get_status_display()})"