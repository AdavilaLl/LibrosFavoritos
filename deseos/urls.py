from django.urls import path     
from . import views_forms

app_name = 'wishes'

urlpatterns = [
    path('', views_forms.main, name='main' ),
    path('login', views_forms.login, name='login'),
    path('exit', views_forms.logout, name='logout'),
    path('wishes', views_forms.mywishes, name='mywishes'),
    path('wishes/stats', views_forms.stats, name='stats'),
    path('wishes/new', views_forms.addWish, name='addWish'),
    path('wishes/<int:id>/delRelUsBK', views_forms.unFavourite, name='deleteRelWishUser'),
    path('wishes/edit/<int:id>', views_forms.editWish, name='editWish'),
    path('wishes/<int:id>/delete', views_forms.delete, name='deleteWish'),
    path('wishes/<int:id>/grantWishUser', views_forms.relationWishToUser, name='relWishUser'),
    path('wishes/<int:id>/like', views_forms.likeWish, name='likeWish'),




]