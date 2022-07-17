from wsgiref import validate
from django.contrib.auth import password_validation, authenticate
import re
import email
from django.core import exceptions
import django.contrib.auth.password_validation as validators
import sys
from rest_framework import serializers
from rest_framework.authtoken.models import Token


from .models import Usuario, Reserva, Pago, Ciudad, Avion, Vuelo
from icarusProjectApp.models import (

    Usuario,
    Vuelo,
    Ciudad,
    Avion,
    Pago,
    
)


class PagoSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Pago.

    """

    class Meta:
        model = Pago
        fields = '__all__'

class AvionSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Avion.
    
    """

    class Meta:
        model = Avion
        fields = '__all__'

class VueloSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Vuelo.
    
    """
    
    class Meta:
        model = Vuelo
        fields = '__all__'

class VueloCustomSerializer(serializers.Serializer):

    """
    Serializer del modelo Vuelo que considera campos en específico.
    
    """

    fecha_salida = serializers.DateField(required = True)
    hora_salida = serializers.TimeField(required = True)
    fecha_llegada = serializers.DateField(required = True)
    hora_llegada = serializers.TimeField(required = True)
    valor_vuelo = serializers.IntegerField(required = True)
    id_ciudad_origen = serializers.IntegerField(required = True)
    id_ciudad_destino = serializers.IntegerField(required = True)
    id_avion_asociado = serializers.IntegerField(required = True)

    def validando_vuelo(data):

        """
        Revisa que el vuelo que esté siendo creado no esté registrado previamente.
    
        """

        if Vuelo.objects.filter(fecha_salida = data['fecha_salida'], hora_salida = data['hora_salida'], fecha_llegada = data['fecha_llegada'], hora_llegada = data['hora_llegada'],  id_ciudad_origen = data['id_ciudad_origen'], id_ciudad_destino = data['id_ciudad_destino'], id_avion_asociado = data['id_avion_asociado']).exists():
            raise serializers.ValidationError({'numero': '1', 'mensaje': 'Este vuelo ya ha sido registrado. Intente nuevamente.'})
        else:
            return True       

    def validando_ciudad(data):

        """
        Revisa que las ciudades ingresadas no sean las mismas.
    
        """

        if (data['id_ciudad_origen'] == data['id_ciudad_destino']):
            raise serializers.ValidationError({'numero': '2', 'mensaje': 'No se puede tener la misma ciudad de origen como destino. Intente nuevamente.'})
        else:
            return True

    def validando_avion_asociado(data):

        """
        Revisa que el avión que se esté registrando en un vuelo no esté programado para esa fecha y hora.
    
        """

        if Vuelo.objects.filter(fecha_salida = data['fecha_salida'], hora_salida = data['hora_salida'], fecha_llegada = data['fecha_llegada'], hora_llegada = data['hora_llegada'], id_avion_asociado=data['id_avion_asociado']).exists():
            raise serializers.ValidationError({'numero': '3', 'mensaje': 'No se puede registrar este avión para esas fechas. Intente nuevamente.'})
        else:
            return True

class CiudadSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Ciudad.
    
    """

    class Meta:
        model = Ciudad
        fields = '__all__'

class CiudadCustomSerializer(serializers.Serializer):

    """
    Serializer del modelo Ciudad que considera campos en específico.
    
    """
    
    nombre = serializers.CharField(required = True)
    pais = serializers.CharField(required = True)



class AvionCustomSerializer(serializers.Serializer):

    """
    Serializer del modelo Avión que considera campos en específico.
    
    """

    modelo = serializers.CharField(required = True)
    capacidad = serializers.IntegerField(required = True)

class UsuarioTokenSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Usuario que considera campos en específico.
    
    """
    class Meta:
        model = Usuario
        fields = ('rut','email','nombre','rol')

class UsuarioSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Usuario.
    
    """
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
    def validate(self, data):         
         user = Usuario(**data)
         
         password = data.get('password')
          
         errors = []
         try:
            if re.search('[0-9]', password) is None:
                errors.append('Error, debe tener al menos un numero')
                     
            if re.search('[A-Z]', password) is None:
                errors.append('Error, debe tener al menos una MAYUSCULA')
                
            validators.validate_password(password=password, user=user)
         
        
         except exceptions.ValidationError as e:
            errors.append('Error, debe contener al menos 8 Caracteres')
             
         
         if errors:
             raise serializers.ValidationError(errors)
          
         return super(UsuarioSerializer, self).validate(data)

class ReservaSerializer(serializers.ModelSerializer):

    """
    Serializer del modelo Reserva.
    
    """

    class Meta:
        model = Reserva
        fields = '__all__'

class ReservaCustomSerializer(serializers.Serializer):

    """
    Serializer del modelo Reserva que considera campos en específico.
    
    """
    
    fecha_reserva = serializers.DateField(required = True)
    valor_reserva = serializers.IntegerField(required = True)
    vuelo = serializers.IntegerField(required = True)
    rut_usuario = serializers.IntegerField(required = True)


    
