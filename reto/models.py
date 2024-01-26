'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Agrega el argumento related_name en los campos groups y user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='reto_users', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='reto_users', blank=True)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)

class UsuarioSucursal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class Evento(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    
class Participante(models.Model):
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    cedula = models.CharField(max_length=15)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    puntos = models.IntegerField()
    fecha = models.DateField()
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, default=1)

'''
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Agrega el argumento related_name en los campos groups y user_permissions
    groups = models.ManyToManyField('auth.Group', related_name='reto_users', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='reto_users', blank=True)

class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)

class UsuarioSucursal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)

class Evento(models.Model):
    OPCIONES_RECORD = [
        ('puntaje', 'Puntaje'),
        ('tiempo', 'Tiempo'),
    ]
    
    OPCIONES_PARTICIPACION = [
        ('unico_evento', 'Único evento'),
        ('unico_dia', 'Único por día'),
        ('unico_semana', 'Único por semana'),
        ('unico_mes', 'Único por mes'),
    ]
    
    OPCIONES_STATUS = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE, default=1)
    record = models.CharField(max_length=10, choices=OPCIONES_RECORD, null=True)
    participacion = models.CharField(max_length=20, choices=OPCIONES_PARTICIPACION, null=True)
    status = models.CharField(max_length=10, choices=OPCIONES_STATUS, null=True)
    tiene_categoria = models.BooleanField(default=False, null=True)
    tiene_subcategoria = models.BooleanField(default=False, null=True)    

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)

class Subcategoria(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)

    
class Participante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    ciudad = models.CharField(max_length=15, null=True)
    cedula = models.CharField(max_length=15)
    fecha = models.DateField()
    tieneci = models.BooleanField(null=True)
    ultima_participacion = models.DateTimeField(null=True)
    
class Representante(models.Model):
    participante = models.OneToOneField(Participante, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=15)
    ciudad = models.CharField(max_length=15, null=True)
    fecha_nacimiento = models.DateField(null=True)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    parentezco = models.CharField(max_length=100)
    
class Puntaje(models.Model):
    fecha = models.DateField()
    marca = models.IntegerField(null=True)
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE, null=True)