from django.db import models

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
    book_text = models.TextField(blank=True, null=True, verbose_name="Текст книги")
    book_file = models.FileField(upload_to="book_files/", blank=True, null=True, verbose_name="Файл книги")

    def __str__(self):
        return self.bookName

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