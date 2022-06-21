from multiprocessing import managers
from pyexpat import model
from re import T

from django.db import models

class Usuario(models.Model):
    rut = models.CharField(primary_key = True, max_length = 255, unique = True)
    nombre = models.CharField(max_length = 255)
    apellido = models.CharField(max_length = 255)
    email = models.EmailField(max_length = 255)
    password = models.CharField(max_length = 255)
    rol = models.IntegerField()
    sexo = models.CharField(max_length = 255)
    telefono = models.IntegerField()
    fecha_nacimiento = models.DateField()
    
    class Meta:
        managed = True

class Reserva(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    solo_ida = models.BooleanField()
    fecha_reserva = models.DateField()
    valor_reserva = models.IntegerField()
    rut_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE
    )

    class Meta:
        managed = True

class Pago(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    tarjeta_credito = models.CharField(max_length = 255)
    numero_tarjeta = models.BigIntegerField()
    fecha_nacimiento = models.DateField()
    cvc = models.IntegerField()
    rut_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE
    )
    id_reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = True

class Ciudad(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    nombre = models.CharField(max_length = 255)
    pais = models.CharField(max_length = 255)

    class Meta:
        managed = True

class Avion(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    modelo = models.CharField(max_length = 255)
    capacidad = models.IntegerField()

    class Meta:
        managed = True

class Vuelo(models.Model):
    id = models.AutoField(primary_key = True, unique = True)
    fecha_salida = models.DateField()
    fecha_llegada = models.DateField()
    id_ciudad_origen = models.ForeignKey(
        Ciudad,
        related_name = 'ciudad_origen',
        on_delete=models.CASCADE
    )
    id_ciudad_destino = models.ForeignKey(
        Ciudad,
        related_name= 'ciudad_destino',
        on_delete=models.CASCADE
    )
    id_avion_asociado = models.ForeignKey(
        Avion,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = True

class Reserva_Vuelo (models.Model):
    id_reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE
    )
    id_vuelo = models.ForeignKey(
        Vuelo,
        on_delete=models.CASCADE
    )

    class Meta:
        managed = True


