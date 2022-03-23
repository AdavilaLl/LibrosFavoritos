import decimal
from email.policy import default
from logging import raiseExceptions
from operator import is_
from wsgiref.validate import validator
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import User, Product, Category, BoletaDetalle, Boleta
import re
import bcrypt
from datetime import date
from django.db.models import Q,Sum


class UserForm(forms.ModelForm):
    confirmar_password = forms.CharField(label='Confirmar Password', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Confirmar Contraseña'}))
    

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
        fields = ['first_name', 'last_name', 'email', 'baby_birthday','typeUser', 'password']

        labels = {
            'first_name':'Nombre:',
            'last_name':'Apellido:',
            'email': 'Email:',
            'password': 'Password:',
            'baby_birthday': 'Cumpleaños del bebe:',
            'typeUser': 'Tipo Usuario:',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Apellido'}),
            'email':forms.TextInput(attrs={'class': 'form-control','placeholder':'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Contraseña'}),
            'baby_birthday': forms.DateInput(attrs={'class': 'form-control', 'type':'date', 'max':date.today().strftime('%Y-%m-%d'),'placeholder':'Dia de nacimiento del Bebe'}),
            'typeUser': forms.Select(attrs={'class': 'form-control'})
        }

class LoginForm(forms.Form):

    correo = forms.CharField(
        label=("Correo"), 
        max_length=100, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Correo'}),
        )
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'password'}))

class ProductForm(forms.ModelForm):

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

    class Meta:

        model = Product
        fields = ['name', 'description', 'price', 'img','size', 'stock', 'prodCat', 'prodGender' ]

        labels = {
            'name':'Nombre:',
            'description':'Descripción:',
            'price': 'Precio:',
            'size': 'Talla:',
            'img': 'Subir imagen:',
            'stock': 'Stock:',
            'prodCat': 'Categoría:',
            'prodGender': 'Género:',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'price':forms.TextInput(attrs={'class': 'form-control'}),
            'size':forms.Select(attrs={'class': 'form-control'}),
            'img':forms.FileInput(attrs={'class': 'form-control'}),
            'stock':forms.TextInput(attrs={'class': 'form-control'}),
            'prodCat':forms.Select(attrs={'class': 'form-control'}),
            'prodGender':forms.Select(attrs={'class': 'form-control'}),


        }

class CategoryForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        length = len(name)
        if length < 3:
            print(length)
            raise forms.ValidationError(
                    f'El nombre debe tener por lo menos 3 caracteres',
                )
        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Nombre requerido',
                )
        return name

    class Meta:

        model = Category
        fields = ['name']

        labels = {
            'name':'Nombre:',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }        

##### Metodos ###########
def login(request):

    if request.method == 'GET':
        #if 'usuario' in request.session:
        #    messages.info(request,'Estas logueado')
        #    return redirect('/')
        #else:
            return render(request, 'baby/login.html' , {'formLogin'  : LoginForm(),})

    if request.method == "POST":
        print(request.POST)
        form = LoginForm(request.POST)

        if form.is_valid():
            user = User.objects.filter(email=form.cleaned_data['correo']).first()
            if user:
                form_password = form.cleaned_data['password']
                if bcrypt.checkpw(form_password.encode(), user.password.encode()):
                    request.session['usuario'] = {'nombre':user.first_name , 'apellido':user.last_name, 'email':user.email, 'id':user.id, 'typeUser':user.typeUser}
                    print(request.session['usuario'])
                    print(request.session['usuario']['typeUser'])
                    if request.session['usuario']['typeUser'] == '1':
                        return redirect(reverse('baby:adminPage'))
                    elif request.session['usuario']['typeUser'] == '3':
                        return redirect(reverse('baby:adminPage'))
                    else:
                        return redirect(reverse('baby:mainPage'))

                else:
                    messages.error(request,'Contraseña o Email invalido')
                    return redirect(reverse('baby:login'))
            else:
                messages.error(request,'Contraseña o Email invalido')
                return redirect(reverse('baby:login'))
        else:
            #messages.error(request,'Con errores, validar nuevamente')
            return render(request, 'baby/login.html', {'formLogin'  : form})

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')

def register(request):
    if request.method == 'GET':
        contexto = {
            'userForm'  : UserForm(),
            }
        return render(request, 'baby/register.html' , contexto)
    if request.method == 'POST':
        form = UserForm(request.POST)
        print(form)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            print(usuario.password)
            usuario.typeUser='2'
            print(usuario)
            usuario.save()
            messages.success(request,'Usuario creado correctamente')
            return redirect(reverse('baby:login'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/register.html', {'userForm'  : form}) 


def mainPage(request):
    if request.method == 'GET':
        productos = Product.objects.all()
        if 'usuario' in request.session:
            boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
            cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid)
        else:
            cart = 0
        contexto = {
            'productos': productos,
            'cart':cart,
            }
        return render(request, 'baby/mainPage.html', contexto)

def productGrid(request):
    if request.method == 'GET':
        allProduct = Product.objects.all()
        prodByPijamasCat = Product.objects.filter(prodCat__name= "Pijamas")
        prodByBodyCat = Product.objects.filter(prodCat__name= "Body")
        prodByConjuntoCat = Product.objects.filter(prodCat__name= "Conjunto")
        prodByBabitasCat = Product.objects.filter(prodCat__name= "Babita")
        prodByInviernoCat = Product.objects.filter(prodCat__name= "Invierno")
        print(prodByInviernoCat)
    return render(request, 'baby/products.html')


def productBySize(request, size):
    if request.method == 'GET':
        cat = Category.objects.all()
        contexto = {
            'size':size,
            'categories':cat,
        }

        return render(request, 'baby/productBySize.html', contexto)

def productBySizeByCat(request, size, category):
    prod = Product.objects.filter(size__in=size)
    if request.method == 'GET':
        print(size)
        print(category)
        prod = Product.objects.filter(prodCat__name= category).filter(size__contains=size)
        contexto = {
            'size':size,
            'category':category,
            'products':prod,
        }
        print(prod)
        return render(request, 'baby/productBySizeByCat.html', contexto)

subtotal = 0
descuento = 0
opGravada = 0
igv = 0.18
precioEnvio = 0

def addToShoppingCart(request, id):
    
    if request.method == 'POST':
        user = User.objects.get(id = request.session['usuario']['id'])
        product = Product.objects.get(id=id)
        cantidad = request.POST['cantidad']
        precioU = product.price
        subtotal = product.price * int(cantidad)
        igvProd = decimal.Decimal(subtotal) * decimal.Decimal(igv)
        opGravada = subtotal - igvProd
        existeBoleta = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        print (existeBoleta)

        if existeBoleta:
            a = 0
        else:
            Boleta.objects.create(total = 0, totalDesc = 0, totalOpGravada = 0, totalIGV = 0, users = user )
        product.cantVendidos = product.cantVendidos+1
        product.stock = product.stock-1
        product.save()
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        print(boletaid)
        BoletaDetalle.objects.create(subtotal = subtotal, descuento = descuento, opGravada = opGravada, igv = igvProd, precioUni=precioU , usuario = user,cantidad = cantidad, estado = True, productos = product, boleta = boletaid)


        #raise Exception('Prueba')


        messages.success(request, 'Producto agregado al carrito')
        return redirect(reverse('baby:shoppingCart'))

def shoppingCart(request):
    if request.method == 'GET':
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid)

        a = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_subtotal = Sum('subtotal'))
        b = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_dsc = Sum('descuento'))
        c = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_igv = Sum('igv'))
        d = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_op_grav = Sum('opGravada'))
        
        descuento = round(b['total_dsc'],2)
        igv = round(c['total_igv'],2)
        op_gravada = round(d['total_op_grav'],2)
        subtotal = round(a['total_subtotal'],2) + 10

        print(cart)
        print(subtotal)
        contexto={
            'cart':cart, 
            'op_gravada': op_gravada,
            'igv':igv,
            'subtotal':subtotal,
            'descuento':descuento,

        }
        return render(request, 'baby/shoppingCart.html', contexto)


def shoppingCartempty(request):
    return render(request, 'baby/shoppingCartEmpty.html')

def buy(request):
    if request.method == 'POST':
        
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'])
        a = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_subtotal = Sum('subtotal'))
        b = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_dsc = Sum('descuento'))
        c = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_igv = Sum('igv'))
        d = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_op_grav = Sum('opGravada'))
        
        subtotal = round(a['total_subtotal'],2) + 10
        descuento = round(b['total_dsc'],2)
        igv = round(c['total_igv'],2)
        op_gravada = round(d['total_op_grav'],2)
        

        boletaid.total = subtotal
        boletaid.totalDesc = descuento
        boletaid.totalOpGravada = op_gravada
        boletaid.totalIGV = igv
        boletaid.pagado = True
        boletaid.save()
        messages.success(request, 'Compra efectuada correctamente')
        return redirect(reverse('baby:mainPage'))

#Admin
def adminMainPage(request):
    #if request.session.usuario.typeUser == '1':
        if request.method == 'GET':
            return render(request, 'baby/indexAdmin.html')



def showUsers(request):
    if request.method == 'GET':
        users = User.objects.all()
        contexto = {
            'users':users
            }
        return render(request, 'baby/adminUsersPage.html', contexto)

def addUserAdmin(request):
    if request.method == 'GET':
        contexto = {
            'userForm'  : UserForm(),
            }
        return render(request, 'baby/addUser.html' , contexto)
    if request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.password = bcrypt.hashpw(usuario.password.encode(), bcrypt.gensalt()).decode()
            print(usuario.password)
            usuario.save()
            messages.success(request,'Usuario creado correctamente')
            return redirect(reverse('baby:showUsers'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/addUser.html', {'userForm'  : form}) 

def editUser(request,id):
    user = User.objects.get(id=id)
    if request.method == 'GET':
        form = UserForm(instance=user)
        context = {
            'userForm':form,
            'user':user
        }
        return render(request, 'baby/editUser.html', context)

    if request.method == "POST":
        print(request.POST)
        user = User.objects.get(id=id)
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario editado correctamente')
            return redirect('baby:showUsers')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/editUser.html', {'userForm'  : form, 'user':user}) 

def deleteUser(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        print(user.first_name)
        user.delete()
        messages.success(request,"Usuario Eliminado correctamente")
        return redirect(reverse('baby:showUsers'))

def adminShowProductsPage(request):
    if request.method == 'GET':
        prod = Product.objects.all()
        contexto = {
            'ProductForm'  : ProductForm(),
            'productos': prod
            }
        return render(request, 'baby/adminProductsPage.html', contexto )

def addProduct(request):
    if request.method == 'GET':
        contexto = {
            'ProductForm'  : ProductForm(),
            }
        return render(request, 'baby/addProduct.html', contexto )
    if request.method == "POST":
        form = ProductForm(request.POST)
        img = ProductForm(request.FILES)
        a = (request.FILES.get('img'))
        if form.is_valid():
            prod = form.save(commit=False)
            prod.img = a
            prod.save()
            print(prod)
            messages.success(request, 'Producto agregado correctamente')
            return redirect(reverse('baby:showProducts'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/addProduct.html', {'ProductForm'  : form}) 

def editProd(request,id):
    prod = Product.objects.get(id=id)
    if request.method == 'GET':
        form = ProductForm(instance=prod)
        context = {
            'ProductForm':form,
            'product':prod
        }
        return render(request, 'baby/editProduct.html', context)

    if request.method == "POST":
        prod = Product.objects.get(id=id)
        form = ProductForm(request.POST,instance=prod)
        img = request.FILES.get('img')
        print(img)
        if form.is_valid():
            p = form.save(commit=False)
            p.img = img
            p.save()
            messages.success(request, 'Producto editado correctamente')
            return redirect('baby:showProducts')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/storeKeeperProductsPage.html', {'ProductForm'  : form}) 

def deleteProd(request, id):
    if request.method == 'POST':
        prodD = Product.objects.get(id=id)
        print(prodD.name)
        prodD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('baby:showProducts'))

def addCategory(request):
    if request.method == 'GET':
        cat = Category.objects.all()
        contexto = {
            'CategoryForm'  : CategoryForm(),
            'categories':cat,
            }

        return render(request, 'baby/addCategory.html' , contexto)
    if request.method == "POST":
        cat = Category.objects.all()
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria creada correctamente')
            return redirect(reverse('baby:addCategory'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/addCategory.html', {'CategoryForm'  : form, 'categories':cat,}) 

def editCat(request,id):
    cat = Category.objects.get(id=id)
    if request.method == 'GET':
        form = CategoryForm(instance=cat)
        context = {
            'CategoryForm':form,
            'category':cat
        }
        return render(request, 'baby/editCategory.html', context)

    if request.method == "POST":
        print(request.POST)
        cat = Category.objects.get(id=id)
        form = CategoryForm(request.POST,instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada correctamente')
            return redirect('baby:addCategory')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'baby/addCategory.html', {'CategoryForm'  : form}) 

def deleteCat(request, id):
    if request.method == 'POST':
        catD = Category.objects.get(id=id)
        print(catD.name)
        catD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('baby:addCategory'))

def showProductDetail(request,id):
    if request.method == 'GET':
        prod = Product.objects.get(id=id)
        contexto = {
            'producto':prod
        }
        print(prod.img)
        return render(request, 'baby/showProductDetail.html', contexto) 


