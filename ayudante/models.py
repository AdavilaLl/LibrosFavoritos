from tkinter import CASCADE
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, verbose_name='contrasenia')

    def __str__(self):
        return f'{self.first_name} , {self.last_name}'

class Job(models.Model):
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    userJob = models.ForeignKey(User,related_name='jobs',on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User,related_name='jobs_created_by',on_delete=models.CASCADE, default=None)