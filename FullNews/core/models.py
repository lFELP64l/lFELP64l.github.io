from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
User = get_user_model()


class CateNew(models.Model):
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return self.descripcion
    
    
class EstadoNew(models.Model):
    descripcion = models.CharField(max_length=30)
    
    def __str__(self):
        return self.descripcion
    
    
class New(models.Model):
    titulo = models.CharField(max_length=200)
    categoria = models.ForeignKey(CateNew, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    texto = models.TextField()
    imagen1 = models.ImageField(default='media/deafultUser.png', upload_to='users/', blank=False)
    imagen2 = models.ImageField(upload_to='users/', null=True, blank=True)
    imagen3 = models.ImageField(upload_to='users/', null=True, blank=True)
    ubicacion = models.CharField(max_length=200, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    estadoNew = models.ForeignKey(EstadoNew, on_delete=models.CASCADE, default=1)
    mensaje = models.TextField(max_length=2000, blank=True, default='no hay revisiones')
    
    def __str__(self):
        return self.titulo
    
    def autor_username(self):
        return self.autor.first_name
    
    def estado(self):
        return self.estadoNew.descripcion
    
    def get_categoria(self):
        return self.categoria.descripcion


class Producto(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name

class carritoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Producto, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.user.first_name

