from django.db import models

# Create your models here.

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, verbose_name='contrasenia')

    def __str__(self):
        return f'{self.first_name} , {self.last_name}'

class Wish(models.Model):
    item = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wished_by = models.ForeignKey(User, related_name='wishes_uploaded', on_delete=models.CASCADE)
    users_who_granted = models.ManyToManyField(User, related_name='granted_wishes')
    users_who_liked = models.ManyToManyField(User, related_name='liked_wishes')
    def __str__(self):
        return f'{self.item}'
