
from pickle import TRUE
import re
from urllib import response

# DJANGO REST framework
from rest_framework import viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


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








""" 
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioViewSetLog(viewsets.GenericViewSet):

    queryset = Usuario.objects.filter()
    serializer_class = UsuarioSerializer

    #detail define si es una peticion de detalle o no, en methods añadimos el metodo permitido, en nuestro caso solo vamo a permitir el post
    @action(detail=False, methods=['post'])
    def login(self, request):
        

        serializer = UsuarioLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        usuario, token = serializer.save()

        data ={
            'usuario': UsuarioSerializer(usuario).data,
            'access_token': token

        }
        return Response(data, status=status.HTTP_201_CREATED)


 """

