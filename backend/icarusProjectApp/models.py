from multiprocessing import managers
from pyexpat import model
from re import T
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UsuarioManager(BaseUserManager):
    def create_user(self,email,nombre,password = None):
        if not email:
            raise ValueError('Debe tener email')

        usuario =self.model(nombre=nombre,email=self.normalize_email(email))

        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self,nombre,email,password):
        usuario =self.create_user(email=self.normalize_email(email),nombre=nombre, password=password)

        usuario.usuario_administrador =True
        usuario.save()
        return usuario

class Usuario(AbstractBaseUser):

    """
    Este es el modelo del Usuario.

    Campos:
        rut {varchar} -- texto en formato rut chileno
        nombre {varchar} -- texto con el nombre del usuario
        apellido {varchar} -- texto con el apellido del usuario
        email {email} -- email que contiene el del usuario
        password {varchar} -- texto con el password del usuario
        rol {integer} -- numero que indica el rol del usuario, 0 admin, 1 cliente
        sexo {varchar} -- texto que indica el sexo del usuario
        telefono {integer} -- numero que indica el telefono del usuario
        fecha_nacimiento {date} -- fecha que indica la fecha de nacimiento del usuario

    """
    nombre =models.CharField(max_length = 255, unique= True, null=True)
    apellido = models.CharField(max_length = 255, null= True)
    email = models.EmailField(max_length = 255, unique= True)
    #password = models.CharField(max_length = 255)
    rut = models.CharField(primary_key = True, max_length = 255, unique = True)
    rol = models.IntegerField(null= True)
    sexo = models.CharField(max_length = 255,null= True)
    telefono = models.IntegerField(null= True)
    fecha_nacimiento = models.DateField(null= True)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default= False)
    objects= UsuarioManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS= ['']
    
    class Meta:
        managed = True


    def __str__(self):
        return f'{self.nombre}'
    
    def has_perm(self,perm,obj = None):
        return True

    def has_module_perms(self,app_label):
        return True
    
    @property
    def is_staff(self):
        return self.usuario_administrador


        
class Reserva(models.Model):

    """
    Este es el modelo de la Reserva.

    Campos:
        id {autoincrement} -- numero de la reserva, que se va autoincrementando
        solo_ida {boolean} -- booleano que indica si la reserva es solamente de ida, 0 solo ida, 1 ida y vuelta
        fecha_reserva {datetime} -- fecha y hora que indica cuando se hizo la reserva
        valor_reserva {integer} -- numero que indica el valor de la reserva
        rut_usuario {foreign} -- relacion con el rut del modelo Usuario

    """

    id = models.AutoField(primary_key = True, unique = True)
    solo_ida = models.BooleanField()
    fecha_reserva = models.DateTimeField()
    valor_reserva = models.IntegerField()
    rut_usuario = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE
    )

    class Meta:
        managed = True

class Pago(models.Model):

    """
    Este es el modelo del Pago.

    Campos:
        id {autoincrement} -- numero de transaccion que identifica el pago, el cual se va autoincrementando
        tarjeta_credito {varchar} -- texto que indica el tipo de tarjeta
        numero_tarjeta {integer} -- numero de la tarjeta de credito
        fecha_vencimiento {date} -- fecha de vencimiento de la tarjeta
        cvc {integer} -- numero de cvc de la tarjeta
        rut_usuario {foreign} -- relacion con el rut del modelo Usuario
        id_reserva {foreign} -- relacion con el id de reserva del modelo Reserva

    """

    id = models.AutoField(primary_key = True, unique = True)
    tarjeta_credito = models.CharField(max_length = 255)
    numero_tarjeta = models.BigIntegerField()
    fecha_vencimiento = models.DateField()
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

    """"
    Este es el modelo de la Ciudad.

    Campos:
        id {autoincrement} -- numero que identifica las ciudades, que se autoincrementa a medida que se ingresan más ciudades
        nombre {varchar} -- texto que indica el nombre de la ciudad
        pais {varchar} -- texto que indica el nombre del pais de la ciudad
    
    """

    id = models.AutoField(primary_key = True, unique = True)
    nombre = models.CharField(max_length = 255)
    pais = models.CharField(max_length = 255)

    class Meta:
        managed = True

class Avion(models.Model):

    """"
    Este es el modelo del Avion.

    Campos: 
        id {autoincrement} -- numero que identifica al avion, que se autoincrementa a medida que se ingresan más aviones
        modelo {varchar} -- texto que indica el modelo del avion
        capacidad {integer} -- numero que indica la capacidad del avion
    
    """

    id = models.AutoField(primary_key = True, unique = True)
    modelo = models.CharField(max_length = 255)
    capacidad = models.IntegerField()

    class Meta:
        managed = True

class Vuelo(models.Model):

    """
    Este es el modelo del Vuelo.

    Campos:
        id {autoincrement} -- numero que identifica al vuelo, que se autoincrementa a medida que se ingresan más vuelos
        fecha_salida {datetime} -- fecha y hora de salida del vuelo
        fecha_llegada {datetime} -- fecha y hora de llegada del vuelo
        id_ciudad_origen {foreign} -- relacion con la ciudad del modelo Ciudad
        id_ciudad_destino {foreign} -- relacion con la ciudad del modelo Ciudad
        id_avion_asociado {foreign} -- relacion con el id del avion del modelo Avion

    """

    id = models.AutoField(primary_key = True, unique = True)
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField()
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

    """
    Este es el modelo Reserva_Vuelo.

    Campos:
        id_reserva {foreign} -- relacion con la id de reserva del modelo Reserva
        id_vuelo {foreign} -- relacion con la id del vuelo del modelo Vuelo

    """

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


