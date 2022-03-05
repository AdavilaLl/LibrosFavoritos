from django.urls import path     
from . import views_forms

app_name = 'books'

urlpatterns = [
    path('', views_forms.main, name='main' ),
    path('login', views_forms.login, name='login'),
    path('exit', views_forms.logout, name='logout'),
    path('books', views_forms.mybooks, name='mybooks'),
    path('books/<int:id>/delRelUsBK', views_forms.unFavourite, name='deleteRelBookUser'),
    path('books/<int:id>', views_forms.bookDetail, name='bookDetail'),
    path('books/<int:id>/delete', views_forms.delete, name='deleteBook'),
    path('books/<int:id>/relBookUser', views_forms.relationBookToUser, name='relBookUser'),



]