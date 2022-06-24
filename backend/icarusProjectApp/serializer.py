#app para que pueda ser consumida por la rest api


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



#serializers que definen la representacion de la api


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model =Usuario
        fields = '__all__'
    def create(self,validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


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










""" 



class UsuarioLoginSerializer(serializers.Serializer):

    #campos que vamos a necesitar
    email = serializers.EmailField()
    password = serializers.CharField()

    #primero validamos los datos
    def valide(self, data):

        # authenticate recibe las credenciales, si son validas devuelve el objeto del usuario
        usuario = authenticate(email=data['email'], password=data['password'])
        if not usuario:
            raise serializers.ValidationError('las credenciales no son validas')

        #guardamos el usuario en el contexto para posteriormente en create recuperar el token
        self['usuario'] = usuario
        return data

    def create(self, data):
        #generar o recuperar token
        token, created =Token.objects.get_or_create(usuario=self.context['usuario'])
        return self.context['usuario'], token.key




class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model =Reserva
        fields = '__all__'



class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model =Pago
        fields = '__all__'

 """