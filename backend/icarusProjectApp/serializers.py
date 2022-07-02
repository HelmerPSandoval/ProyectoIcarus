#Django
from wsgiref import validate
from django.contrib.auth import password_validation, authenticate

import email
#from platformdirs import user_cache_dir
#Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token


#models
from .models import Usuario, Reserva, Pago, Ciudad, Avion, Vuelo, Reserva_Vuelo
from icarusProjectApp.models import (

    Usuario,
    Vuelo,
    Ciudad,
    Avion,
)

#serializers que definen la representacion de la api

class AvionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avion
        fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):
    
     class Meta:
        model = Vuelo
        fields = '__all__'

class VueloCustomSerializer(serializers.Serializer):

    fecha_salida = serializers.DateField(required = True)
    hora_salida = serializers.TimeField(required = True)
    fecha_llegada = serializers.DateField(required = True)
    hora_llegada = serializers.TimeField(required = True)
    id_ciudad_origen = serializers.IntegerField(required = True)
    id_ciudad_destino = serializers.IntegerField(required = True)
    id_avion_asociado = serializers.IntegerField(required = True)

    def validando_vuelo(data):

        if Vuelo.objects.filter(fecha_salida = data['fecha_salida'], hora_salida = data['hora_salida'], fecha_llegada = data['fecha_llegada'], hora_llegada = data['hora_llegada'],  id_ciudad_origen = data['id_ciudad_origen'], id_ciudad_destino = data['id_ciudad_destino'], id_avion_asociado = data['id_avion_asociado']).exists():
            raise serializers.ValidationError({'numero': '1', 'mensaje': 'Este vuelo ya ha sido registrado. Intente nuevamente.'})
        else:
            return True       

    def validando_ciudad(data):

        if (data['id_ciudad_origen'] == data['id_ciudad_destino']):
            raise serializers.ValidationError({'numero': '2', 'mensaje': 'No se puede tener la misma ciudad de origen como destino. Intente nuevamente.'})
        else:
            return True

    def validando_avion_asociado(data):
        if Vuelo.objects.filter(fecha_salida = data['fecha_salida'], hora_salida = data['hora_salida'], fecha_llegada = data['fecha_llegada'], hora_llegada = data['hora_llegada'], id_avion_asociado=data['id_avion_asociado']).exists():
            raise serializers.ValidationError({'numero': '3', 'mensaje': 'No se puede registrar este avión para esas fechas. Intente nuevamente.'})
        else:
            return True

class CiudadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ciudad
        fields = '__all__'

class CiudadCustomSerializer(serializers.Serializer):
    
    nombre = serializers.CharField(required = True)
    pais = serializers.CharField(required = True)



class AvionCustomSerializer(serializers.Serializer):

    modelo = serializers.CharField(required = True)
    capacidad = serializers.IntegerField(required = True)

class UsuarioTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('rut','email','nombre','rol')

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model =Usuario
        fields = '__all__'
    def create(self,validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario
    def update(self, instance, validated_data):
        updated_usuario = super().update(instance, validated_data)
        updated_usuario.set_password(validated_data['password'])
        updated_usuario.save()
        return updated_usuario

class ReservaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaCustomSerializer(serializers.Serializer):

    tarjeta_credito = serializers.DateField(required = True)
    numero_tarjeta = serializers.TimeField(required = True)
    fecha_vencimiento = serializers.DateField(required = True)
    cvc = serializers.TimeField(required = True)
    rut_usuario = serializers.IntegerField(required = True)
    
class TestUsuarioSerializer(serializers.Serializer):
    rut = serializers.CharField()
    nombre = serializers.CharField()
    email =serializers.EmailField()

    
    def validate_username(self,value):
        # validacion
        if 'developer' in value:
            raise serializers.ValidationError('Error, no puede existir un usuario con este nombre')
        return value


    def validate_email(self,value):
        # validacion
        if value =='':
            raise serializers.ValidationError('tiene que indicar un correo')

        if  self.validate_username(self.context['nombre']) in value:
            raise serializers.ValidationError('El email no puede contener el nombre')

        return value

    def validate(self,data):
        return data


    """ def create(self, validated_data):
        print(validated_data)
        return Usuario.objects.create(**validated_data)
 """
