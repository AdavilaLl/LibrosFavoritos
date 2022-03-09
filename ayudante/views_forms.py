from email.policy import default
from wsgiref.validate import validator
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import User, Job
import re
import bcrypt
from datetime import date
from django.db.models import Q

class UserForm(forms.ModelForm):
    confirmar_password = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        length = len(first_name)

        if length <= 1:
            print(length)
            raise forms.ValidationError(
                    f'El nombre debe tener por lo menos 2 caracteres',
                )

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Nombre requerido',
                )
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        length = len(last_name)

        if length <= 1:
            print(length)
            raise forms.ValidationError(
                    f'El apellido debe tener por lo menos 2 caracteres',
                )
        return last_name

    def clean_password(self):
        password = self.cleaned_data['password']
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if EMAIL_REGEX.match(password) is False: 
            raise forms.ValidationError(
                    f'El email ingresado no cumple con el formato requerido, ingrese nuevamente.',
                )
        return password


    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                    "Las contraseñas no coinciden"
                    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

        labels = {
            'first_name':'Nombre:',
            'last_name':'Apellido',
            'email': 'Email',
            'password': 'Password',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email':forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class LoginForm(forms.Form):

    correo = forms.CharField(
        label=("Correo"), 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Correo'}),
        )
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'password'}))

class JobForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data['title']
        length = len(title)

        if length < 3:
            print(length)
            raise forms.ValidationError(
                    f'El nombre debe tener mas de 3 caracteres.',
                )

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Nombre requerido',
                )
        return title


    def clean_description(self):
        description = self.cleaned_data['description']
        length = len(description)

        if length <= 1:
            print(length)
            raise forms.ValidationError(
                    f'La descripcion debe tener mas de 10 caracteres.',
                )
        return description

    def clean_location(self):
        location = self.cleaned_data['location']
        length = len(location)

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Location no debe quedar vacio.',
                )
        return location


    class Meta:
        model = Job
        fields = ['title', 'description', 'location']

        labels = {
            'title':'Title:',
            'description':'Description',
            'location': 'Location',
            
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location':forms.TextInput(attrs={'class': 'form-control'}),
        }


##### Metodos ###########
def main(request):
    if request.method == 'GET':
        if 'usuario' in request.session:
            messages.info(request,'Estas logueado')
            return redirect(reverse('ayudante:dashboard'))
        else:
            return render(request, 'ayudante/main.html' , {'formRegister'  : UserForm(),'formLogin'  : LoginForm(),})
    
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)


        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            print(usuario.password)
            usuario.save()
            messages.success(request,'Usuario creado correctamente')
            return redirect(reverse('ayudante:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'ayudante/main.html', {'formRegister':form, 'formLogin'  : LoginForm()})

def login(request):

    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['correo']).first()
            if user:
                form_password = form.cleaned_data['password']
                if bcrypt.checkpw(form_password.encode(), user.password.encode()):
                    request.session['usuario'] = {'nombre':user.first_name , 'apellido':user.last_name, 'email':user.email, 'id':user.id}
                    print(request.session['usuario'])
                    return redirect(reverse('ayudante:dashboard'))
                else:
                    messages.error(request,'Contraseña o Email invalido')
                    return redirect(reverse('ayudante:main'))
            else:
                messages.error(request,'Contraseña o Email invalido')
                return redirect(reverse('ayudante:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'ayudante/main.html', {'formRegister':UserForm(), 'formLogin'  : form()})

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')

def dashboard(request):
    user = User.objects.get(id=request.session['usuario']['id'])
    if request.method == "GET":
        jobs = Job.objects.filter(userJob = None)
        myAsignedJobs = Job.objects.filter(userJob = user)
        contexto = {
            'jobs':jobs,
            'myAsignedJobs':myAsignedJobs,
            'user' : user
            }
        return render(request, 'ayudante/dashboard.html', contexto)




def addJob(request):
    if request.method == "GET":
        context = {
            'jobForm':JobForm()
        }
        return render(request, 'ayudante/addJob.html', context)
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            user = User.objects.get(id=request.session['usuario']['id'])
            job.created_by = user
            job.save()
            messages.success(request, 'Trabajo creado correctamente')
            return redirect(reverse('ayudante:dashboard'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ayudante/addJob.html', {'jobForm'  : form})   

def showJob(request, id):
    job = Job.objects.get(id=id)
    user = User.objects.get(id=request.session['usuario']['id'])
    if request.method == "GET":
        context = {
            'job': job,
            'user':user
        }
        return render(request, 'ayudante/showJob.html', context)

def deleteJob(request, id):

    if request.method == 'POST':
        jobD = Job.objects.get(id=id)
        print(jobD.title)
        jobD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('ayudante:dashboard'))

def doneJob(request, id):
    jobD = Job.objects.get(id=id)
    print(jobD.title)
    jobD.delete()
    messages.success(request,"Tarea finalizada correctamente")
    return redirect(reverse('ayudante:dashboard'))

def editJob(request,id):
    job = Job.objects.get(id=id)
    if request.method == 'GET':
        form = JobForm(instance=job)
        context = {
            'jobForm':form
        }
        return render(request, 'ayudante/editJob.html', context)

    if request.method == "POST":
        print(request.POST)
        show = Job.objects.get(id=id)
        form = JobForm(request.POST,instance=show)
        if form.is_valid():
            form.save()
            messages.success(request, 'Trabajo editado correctamente')
            return redirect('ayudante:dashboard')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ayudante/editJob.html', {'jobForm'  : form}) 

def asignJob(request,id):
    user = User.objects.get(id=request.session['usuario']['id'])
    job = Job.objects.get(id=id)
    job.userJob = user
    job.save()
    messages.success(request, f'Trabajo {job.title} agregado a tu lista.')
    return redirect(reverse('ayudante:dashboard'))
