from distutils.command.upload import upload
from django.db import models

# Create your models here.




class User(models.Model):
    TYPEUSER_CHOICES = (
        ('1','ADMINISTRADOR'),
        ('2','USUARIO'),
        ('3','ALMACENERO'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=100, verbose_name='contrasenia')
    baby_birthday = models.DateField(null=True, blank=True)
    typeUser = models.CharField(max_length=1, choices = TYPEUSER_CHOICES, default = '2', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} , {self.last_name}'

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    GENDER_CHOICES = (
    ('1','Niño'),
    ('2','Niña'),
    ('3','Unisex')
    )

    SIZE_CHOICES = (
    ('1','0-3 meses'),
    ('2','3-6 meses'),
    ('3','6-12 meses'),
    ('4','12-18 meses'),
    ('5','18-24 meses'),
    ('6','2 años'),
    ('7','3 años'),    
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=400)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    img = models.ImageField(upload_to="images/", blank=True, null=True)
    size = models.CharField(max_length=50,choices=SIZE_CHOICES, default='0-6 meses')
    stock = models.IntegerField(default=1, null=False)
    prodCat = models.ForeignKey(Category, related_name='productos', on_delete=models.CASCADE)
    prodGender = models.CharField(max_length=1, choices = GENDER_CHOICES, default = '1')
    cantVendidos = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__ (self):
        return f'{self.name} - {self.prodCat.name} - {self.price} - {self.stock}'


class Boleta(models.Model):

    total = models.DecimalField(decimal_places=2, max_digits=6)
    totalDesc = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    totalOpGravada = models.DecimalField(decimal_places=2, max_digits=6)
    totalIGV = models.DecimalField(decimal_places=2, max_digits=6)
    precioEnvio = models.DecimalField(decimal_places=2, max_digits=6, default = 10)
    #detalleBoleta=models.ManyToManyField(BoletaDetalle, related_name='carritos')
    users = models.ForeignKey(User, related_name='usuarios2', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pagado = models.BooleanField(default=False)

    def __str__ (self):
        return f'{self.users} - {self.pagado}'


class BoletaDetalle(models.Model):
    
    precioUni = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=6)
    descuento = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    opGravada = models.DecimalField(decimal_places=2, max_digits=6)
    igv = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(User, related_name='usuarios', on_delete=models.CASCADE)
    productos = models.ForeignKey(Product, related_name='boletaDetalle', on_delete=models.CASCADE, default=0)
    cantidad = models.IntegerField(default=1, null=False)
    estado = models.BooleanField(default=False)
    boleta = models.ForeignKey(Boleta, related_name='boletas', on_delete=models.CASCADE, default =1)
    
    def __str__ (self):
        return f'{self.usuario} - {self.productos} - {self.cantidad} - {self.boleta.id}'


