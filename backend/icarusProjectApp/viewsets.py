
from pickle import TRUE
import re
from urllib import response

# DJANGO REST framework
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from icarusProjectApp.serializer import UsuarioTokenSerializer


# MODELS
from .models import(Usuario)

# SERIALIZERS
from .serializer import(TestUsuarioSerializer, UsuarioSerializer)


@api_view(['GET','POST'])
def usuario_api_view(request):

    # list
    if request.method == 'GET':

        #queryset
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many =True)

        test_data = {
            'rut':'59978950',
            'nombre':'chorizo',
            'email':'test2@gmail.com',
        }

        test_usuario = TestUsuarioSerializer(data = test_data, context =test_data)
        if test_usuario.is_valid():
            print("paso validaciones")
            #usuario_instance = test_usuario.save()
            #print(usuario_instance)
        else: 
            print(test_usuario.errors)

        return Response(usuarios_serializer.data, status = status.HTTP_200_OK)
    
    # create
    elif request.method == 'POST':
        usuario_serializer = UsuarioSerializer(data=request.data)

        # validacion
        if usuario_serializer.is_valid():
            usuario_serializer.save()

            return Response({'message':'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)

        return Response(usuario_serializer.errors, status =status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT','DELETE'])
def usuario_detail_api_view(request,pk=None):

    # consulta
    usuario = Usuario.objects.filter(rut=pk).first()

    # validacion
    if usuario:

        # retrieve
        if request.method == 'GET':            
            usuario_serializer = UsuarioSerializer(usuario)
            return Response(usuario_serializer.data, status = status.HTTP_200_OK)

        #actualizar
        elif request.method == 'PUT':           
            usuario_serializer =UsuarioSerializer(usuario, data =request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                return Response(usuario_serializer.data, status = status.HTTP_200_OK)
            return Response(usuario_serializer.errors, status = status.HTTP_400_BAD_REQUEST)
 
        # eliminar
        elif request.method == 'DELETE':            
            usuario.delete()
            return Response({'message':'Usuario eliminado correctamente!'}, status = status.HTTP_200_OK)

    return Response({'message':'no se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self,request,*args,**kwargs):
        login_serializer = self.serializer_class(data = request.data, context = {'request' :request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.usuario_activo:
                token,created = Token.objects.get_or_create(user = user)
                user_serializer=UsuarioTokenSerializer(user)
                if created:
                    return Response({'token' : token.key, 'user' : user_serializer.data, 'mensaje' : 'Inicio de sesión exitoso'}, status = status.HTTP_201_CREATED)
                else:
                    token.delete()
                    token = Token.objects.create(user = user)
                    return Response({'token' : token.key, 'user' : user_serializer.data, 'mensaje' : 'Inicio de sesión exitoso'}, status = status.HTTP_201_CREATED)
            else:
                return Response({'error':'Este usuario no pude iniciar sesión'}, status = status.HTTP_401_UNAUTHORIZED)
        else:
             return Response({'error':'Nombre de usuario o contraseña incorrectos.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje':'Hola desde response'}, status = status.HTTP_200_OK)

class Logout(APIView):

    def get(self,request,*args,**kwargs):
        token = request.GET.get('token')
        token = Token.objects.filter(key = token).first()
        if token:
            user = token.user 

