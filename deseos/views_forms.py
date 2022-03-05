from email.policy import default
from wsgiref.validate import validator
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import User, Wish
import re
import bcrypt
from datetime import date

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



class WishForm(forms.ModelForm):

    def clean_item(self):
        title = self.cleaned_data['item']
        length = len(title)

        if length <= 3:
            print(length)
            raise forms.ValidationError(
                    f'El deseo debe tener por lo menos 3 caracteres',
                )

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Deseo requerido',
                )

        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        length = len(description)

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Descripcion requerida',
                )

        return description

    class Meta:
        model = Wish
        fields = ['item', 'description']

        labels = {
            'item':'Item:',
            'description':'Descripcion'
        }

        widgets = {
            'item': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

##### Metodos ###########
def main(request):
    if request.method == 'GET':
        if 'usuario' in request.session:
            messages.info(request,'Estas logueado')
            return redirect(reverse('wishes:mywishes'))
        else:
            return render(request, 'deseos/main.html' , {'formRegister'  : UserForm(),'formLogin'  : LoginForm(),})
    
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)


        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            print(usuario.password)
            usuario.save()
            messages.success(request,'Usuario creado correctamente')
            return redirect(reverse('wishes:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'deseos/main.html', {'formRegister':form, 'formLogin'  : LoginForm()})

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
                    return redirect(reverse('wishes:mywishes'))
                else:
                    messages.error(request,'Contraseña o Email invalido')
                    return redirect(reverse('wishes:main'))
            else:
                messages.error(request,'Contraseña o Email invalido')
                return redirect(reverse('wishes:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'deseos/main.html', {'formRegister':UserForm(), 'formLogin'  : form()})

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')


def mywishes(request):
    count = 0
    if request.method == "GET":
        wishes = Wish.objects.all()
        authorwishes = User.objects.get(id=request.session['usuario']['id']).wishes_uploaded.all()
        # Todo los libros que no son del autor
        otherwishes = Wish.objects.all().exclude(wished_by = User.objects.get(id=request.session['usuario']['id']))

        #grantedWishes = Wish.users_who_granted.all()
        #print(grantedWishes)
        granted_wishes = User.objects.get(id=request.session['usuario']['id']).granted_wishes.all()
        user = User.objects.get(id=request.session['usuario']['id'])

        allWishes = Wish.objects.all()
        for a in allWishes:
            print(a)
            print(a.users_who_liked.count())



        return render(request, 'deseos/firstPage.html', {
            'wishes'  : wishes, 
            'wishForm': WishForm(),
            'authorwishes': authorwishes,
            'otherwishes':otherwishes,
            'granted_wishes':granted_wishes,
            'allWishes':allWishes,
        })


    if request.method == "POST":
        print(request.POST)


def addWish(request):

        if request.method == "GET":
            context = {
                'wishForm':WishForm()
            }
            return render(request, 'deseos/makeWish.html', context)

        if request.method == "POST":
            form = WishForm(request.POST)
            if form.is_valid():
                wish=form.save(commit=False)
                user = User.objects.get(id = request.session['usuario']['id'])
                wish.wished_by = user
                wish.save()
                messages.success(request, 'Deseo creado correctamente')
                return redirect(reverse('wishes:mywishes'))
            else:
                messages.error(request, 'Con errores, solucionar.')
                return render(request, 'deseos/makeWish.html', {'formModel'  : form})   

def delete(request,id):
    if request.method == 'POST':
        wishD = Wish.objects.get(id=id)
        print(wishD.item)
        wishD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('wishes:mywishes'))


def relationWishToUser(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['usuario']['id'])
        wish = Wish.objects.get(id=id)
        wish.users_who_granted.add(user)
        messages.success(request,"Deseo concedido!")
        return redirect(reverse('wishes:mywishes'))

def unFavourite(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['usuario']['id'])
        wish = wish.objects.get(id=id)
        wish.users_who_granted.remove(user)
        messages.warning(request,"Se quito el libro de favoritos")
        return redirect(reverse('wishes:mywishes'))

def editWish(request,id):
    wish = Wish.objects.get(id=id)
    if request.method == 'GET':
        form = WishForm(instance=wish)
        context = {
            'wishForm':form
        }
        return render(request, 'deseos/editWish.html', context)

    if request.method == "POST":
        print(request.POST)
        show = Wish.objects.get(id=id)
        form = WishForm(request.POST,instance=show)
        if form.is_valid():
            form.save()
            messages.success(request, 'Deseo editado correctamente')
            return redirect('wishes:mywishes')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'deseo/editWish.html', {'formModel'  : form}) 

def stats(request):
    count = 0
    if request.method == "GET":
        users = User.objects.get(id=request.session['usuario']['id'])
        allGrantedWishes = User.objects.all()
        for a in allGrantedWishes:
            print(a)
            count += a.granted_wishes.count()
        
        allUserWishesGranted = users.granted_wishes.all().count()
        wishUserCount = User.objects.get(id=request.session['usuario']['id']).wishes_uploaded.all().count()
        pendingWishes = wishUserCount-allUserWishesGranted 
        print(allGrantedWishes)
        print(count)
        print(allUserWishesGranted)
        print(wishUserCount)
        return render(request, 'deseos/stats.html', {'users': users, 'pendingWishes': pendingWishes, 'totalGrantedWishes':count})


def likeWish(request, id):
    if request.method=='POST':
        user = User.objects.get(id=request.session['usuario']['id'])
        wish = Wish.objects.get(id=id)
        wish.users_who_liked.add(user)
        messages.success(request,f"Te gusta el deseo:{wish.item} de {user.first_name} {user.last_name}!")
        return redirect(reverse('wishes:mywishes'))