from django.urls import path     
from . import views_forms

app_name = 'ayudante'

urlpatterns = [
    path('', views_forms.main, name='main' ),
    path('login', views_forms.login, name='login'),
    path('exit', views_forms.logout, name='logout'),
    path('dashboard', views_forms.dashboard, name='dashboard'),
    path('addJob', views_forms.addJob, name='addJob'),
    path('showJob/<int:id>', views_forms.showJob, name='showJob'),
    path('edit/<int:id>', views_forms.editJob, name='editJob'),
    path('delete/<int:id>', views_forms.deleteJob, name='deleteJob'),
    path('doneJob/<int:id>', views_forms.doneJob, name='doneJob'),
    path('asignJob/<int:id>', views_forms.asignJob, name='asignJob'),
]