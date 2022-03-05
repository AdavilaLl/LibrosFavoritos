from email.policy import default
from wsgiref.validate import validator
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import User, Book
import re
import bcrypt
from datetime import date

CIERTA_EDAD = 18

def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

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

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        if birthday is not None:
            edad = calculate_age(birthday)
        else:
            edad=0

        if birthday > date.today():
            raise forms.ValidationError(
                    f"solo fechas en pasado."
                )

        if edad < CIERTA_EDAD:
            raise forms.ValidationError(
                    f"La edad es menor a {CIERTA_EDAD}, porque tiene {edad} años."
                )
        return birthday


    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)

        if cleaned_data.get('password') != cleaned_data.get('confirmar_password'):
            raise forms.ValidationError(
                    "Las contraseñas no coinciden"
                    )

    def clean_birthday(self):
        birthday = self.cleaned_data['birthday']
        try:
            edad = calculate_age(birthday)
        except:
            edad=0 

        if birthday > date.today():
            raise forms.ValidationError(
                    f"solo fechas en pasado."
                )

        if edad < CIERTA_EDAD:
            raise forms.ValidationError(
                    f"La edad es menor a {CIERTA_EDAD}, porque tiene {edad} años."
                )
        return birthday

    class Meta:
        model = User
        fields = ['first_name', 'last_name','birthday', 'email', 'password']

        labels = {
            'first_name':'Nombre:',
            'last_name':'Apellido',
            'birthday': 'Fecha de nacimiento',
            'email': 'Email',
            'password': 'Password',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type':'date', 'max':date.today().strftime('%Y-%m-%d')}),
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



class BookForm(forms.ModelForm):

    def clean_title(self):
        title = self.cleaned_data['title']
        length = len(title)

        if length <= 4:
            print(length)
            raise forms.ValidationError(
                    f'El titulo debe tener por lo menos 4 caracteres',
                )

        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Titulo requerido',
                )

        return title

    class Meta:
        model = Book
        fields = ['title', 'description']

        labels = {
            'title':'Titulo:',
            'description':'Descripcion',
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

##### Metodos ###########
def main(request):
    if request.method == 'GET':
        if 'usuario' in request.session:
            messages.info(request,'Estas logueado')
            return redirect(reverse('books:mybooks'))
        else:
            return render(request, 'app/main.html' , {'formRegister'  : UserForm(),'formLogin'  : LoginForm(),})
    
    if request.method == "POST":
        print(request.POST)
        form = UserForm(request.POST)


        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            print(usuario.password)
            usuario.save()
            messages.success(request,'Usuario creado correctamente')
            return redirect(reverse('books:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'app/main.html', {'formRegister':form, 'formLogin'  : LoginForm()})

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
                    return redirect(reverse('books:mybooks'))
                else:
                    messages.error(request,'Contraseña o Email invalido')
                    return redirect(reverse('books:main'))
            else:
                messages.error(request,'Contraseña o Email invalido')
                return redirect(reverse('books:main'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'app/main.html', {'formRegister':UserForm(), 'formLogin'  : form()})

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')


def mybooks(request):

    if request.method == "GET":
        books = Book.objects.all()
        authorBooks = User.objects.get(id=request.session['usuario']['id']).books_uploaded.all()
        # Todo los libros que no son del autor
        # otherBooks = Book.objects.all().exclude(uploaded_by = User.objects.get(id=request.session['usuario']['id']))
        otherBooks = Book.objects.all().exclude(users_who_like = User.objects.get(id=request.session['usuario']['id']))
        favouritesBooks = User.objects.get(id=request.session['usuario']['id']).liked_books.all()
        print(favouritesBooks)
        return render(request, 'app/firstPage.html', {
            'books'  : books, 
            'bookForm': BookForm(),
            'authorBooks': authorBooks,
            'otherBooks': otherBooks,
            'favouritesBooks':favouritesBooks
        }) 

    if request.method == "POST":
        print(request.POST)

        form = BookForm(request.POST)
        if form.is_valid():
            book=form.save(commit=False)
            user = User.objects.get(id = request.session['usuario']['id'])
            book.uploaded_by = user
            book.save()
            book.users_who_like.add(user)
        
            messages.success(request, 'Libro creado correctamente')
            return redirect(reverse('books:mybooks'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'app/firstPage.html', {'formModel'  : form})    


def bookDetail(request,id):

    book = Book.objects.get(id = id)
    if request.session['usuario']['id'] == book.uploaded_by.id:
        print('id sesion:'+str(request.session['usuario']['id'])+' uploadedId:'+str(book.uploaded_by.id))
        if request.method == "GET":
            form = BookForm(instance=book)
            peopleWhoLikeBook = book.users_who_like.all()
            
            return render(request, 'app/showDetailMine.html', {'book': book, 'bookForm':form, 'peopleWhoLikeBook':peopleWhoLikeBook })
        
        if request.method == "POST":
            print(request.POST)
            show = Book.objects.get(id=id)
            form = BookForm(request.POST,instance=show)

            if form.is_valid():
                form.save()
                messages.success(request, 'Libro editado correctamente')
                return redirect('books:bookDetail', id = id)
            else:
                messages.error(request, 'Con errores, solucionar.')
                return render(request, 'app/editShow.html', {'formModel'  : form})    
        
    else:

        print('id sesion:'+str(request.session['usuario']['id'])+' uploadedId:'+str(book.uploaded_by.id))
        if request.method == "GET":
            peopleWhoLikeBook = book.users_who_like.all()
            return render(request, 'app/showDetail.html', {'book': book, 'peopleWhoLikeBook': peopleWhoLikeBook})


def delete(request,id):
    if request.method == 'POST':
        bookD = Book.objects.get(id=id)
        print(bookD.title)
        bookD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('books:mybooks'))


def relationBookToUser(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['usuario']['id'])
        book = Book.objects.get(id=id)
        book.users_who_like.add(user)
        messages.success(request,"Libro añadido a favoritos correctamente")
        return redirect(reverse('books:mybooks'))

def unFavourite(request,id):
    if request.method == 'POST':
        user = User.objects.get(id = request.session['usuario']['id'])
        book = Book.objects.get(id=id)
        book.users_who_like.remove(user)
        messages.warning(request,"Se quito el libro de favoritos")
        return redirect(reverse('books:mybooks'))