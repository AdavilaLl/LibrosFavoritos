from turtle import title
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, verbose_name='contrasenia')
    birthday = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} , {self.last_name}, {self.liked_books}, {self.books_uploaded}'

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name='books_uploaded', on_delete=models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name='liked_books')
    def __str__(self):
        return f'{self.title}'