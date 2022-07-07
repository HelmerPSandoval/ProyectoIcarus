# DJANGO REST framework
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, action

from pickle import TRUE
import re
from urllib import response

import pdfkit
from json2table import convert
from django.http import HttpResponse

from icarusProjectApp.models import (

    Vuelo,
    Ciudad,
    Avion,
    Usuario,
    Reserva,
    Pago,
)

from icarusProjectApp.serializers import (

    VueloSerializer,
    CiudadSerializer,
    VueloCustomSerializer,
    CiudadCustomSerializer,
    AvionSerializer,
    AvionCustomSerializer,
    TestUsuarioSerializer,
    UsuarioSerializer,
    UsuarioTokenSerializer,
    ReservaSerializer,
    ReservaCustomSerializer,
    PagoSerializer,

)

class VueloAPIView(APIView):

    def get(self, request): 
        
        vuelos = Vuelo.objects.all()
        vuelos_serializer = VueloSerializer(vuelos, many = True)
        return Response(vuelos_serializer.data)

    def post(self, request):

        data = request.data

        if (VueloCustomSerializer.validando_vuelo(data) and VueloCustomSerializer.validando_ciudad(data) and VueloCustomSerializer.validando_avion_asociado(data)):
        
            serializer = VueloCustomSerializer(data = request.data)

            if serializer.is_valid():                      

                data_valida = serializer.validated_data
                            
                data_valida["id_ciudad_origen"] = Ciudad.objects.get(id = data_valida["id_ciudad_origen"])
                data_valida["id_ciudad_destino"] = Ciudad.objects.get(id = data_valida["id_ciudad_destino"])
                data_valida["id_avion_asociado"] = Avion.objects.get(id = data_valida["id_avion_asociado"])
                
                vuelo_nuevo = Vuelo.objects.create(**data_valida)
        
                data = VueloSerializer(vuelo_nuevo).data  
                return Response({"Return": 69,"Mensaje": "El vuelo ha sido creado correctamente."})
          

            else:

                data = {'error': str(serializer.errors)}
        else:

            data = {'error': str(serializer.errors)}

        return Response(data = data)
    

class VueloListAPIView(APIView):

    def get(self, request, pk):

        vuelo= Vuelo.objects.get(id = pk)
        vuelo_serializer = VueloSerializer(vuelo)

        return Response(vuelo_serializer.data)

    def put(self, request, pk):

        vuelo = Vuelo.objects.get(id = pk)

        data = request.data

        if (VueloCustomSerializer.validando_vuelo(data) and VueloCustomSerializer.validando_ciudad(data) and VueloCustomSerializer.validando_avion_asociado(data)):

            serializer = VueloSerializer(vuelo, data)

            if serializer.is_valid():

                serializer.save()            

                return Response({"Return": 69,"Mensaje": "El vuelo ha sido editado correctamente."})

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            data = {'error': str(serializer.errors)}

    def delete(self, request, pk):

        vuelo = Vuelo.objects.filter(id = pk)

        vuelo.delete()

        return Response({"Return": 69,"Mensaje": "Se eliminó el vuelo correctamente."})


class CiudadAPIView(APIView):

    def get(self, request):

        ciudades = Ciudad.objects.all()
        ciudades_serializer = CiudadSerializer(ciudades, many = True)
        return Response(ciudades_serializer.data)

    def post(self, request):

        serializer = CiudadCustomSerializer(data = request.data)

        if serializer.is_valid():

            data_valida = serializer.validated_data
            ciudad_nueva = Ciudad.objects.create(**data_valida)

            data = CiudadSerializer(ciudad_nueva).data

        else:

            data = {'error': str(serializer.errors)}

        return Response({"Return": 69,"Mensaje": "La ciudad ha sido creada correctamente."})

class AvionAPIView(APIView):

    def get(self, request):

        aviones = Avion.objects.all()
        aviones_serializer = AvionSerializer(aviones, many = True)
        return Response(aviones_serializer.data)

    def post(self, request):

        serializer = AvionCustomSerializer(data = request.data)

        if serializer.is_valid():

            data_valida = serializer.validated_data
            avion_nuevo = Avion.objects.create(**data_valida)

            data = AvionSerializer(avion_nuevo).data
        else:

            data = {'error': str(serializer.errors)}

        return Response({"Return": 69,"Mensaje": "El vuelo ha sido creado correctamente."})

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

            return Response({"Return": 69,"Mensaje":'Usuario creado correctamente'}, status = status.HTTP_201_CREATED)

        return Response({"Return":70,"Mensaje": usuario_serializer.errors}, status =status.HTTP_400_BAD_REQUEST)


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
                return Response({"Return": 69,"Mensaje":'Usuario modificado correctamente.'}, status = status.HTTP_200_OK)
            return Response({"Return":70,"Mensaje": usuario_serializer.errors}, status = status.HTTP_400_BAD_REQUEST)
 
        # eliminar
        elif request.method == 'DELETE':            
            usuario.delete()
            return Response({"Return":69,"Mensaje": 'Usuario eliminado correctamente!'}, status = status.HTTP_200_OK)

    return Response({"Return":70,"Mensaje":'No se ha encontrado un usuario con estos datos'}, status = status.HTTP_400_BAD_REQUEST)
    


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
        

class Logout(APIView):

    def get(self,request,*args,**kwargs):
        token = request.GET.get('token')
        token = Token.objects.filter(key = token).first()
        if token:
            user = token.user 

@api_view(['GET','POST'])
def reserva_api_view(request):

    # list
    if request.method == 'GET':

        #queryset
        reservas = Reserva.objects.all()
        reservas_serializer = ReservaSerializer(reservas, many =True)
        return Response(reservas_serializer.data, status = status.HTTP_200_OK)
    
    # create
    elif request.method == 'POST':
        reserva_serializer = ReservaSerializer(data=request.data)

        # validacion
        if reserva_serializer.is_valid():

            reserva_serializer.save()     

            input = reserva_serializer.data

            build_direction = "LEFT_TO_RIGHT"

            table_attributes = {"style" : "width:100%"}

            json_to_html = convert(input, build_direction=build_direction, table_attributes=table_attributes)

            config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

            pdfkit.from_string(json_to_html, "reserva.pdf", configuration=config)       
           
            return Response({"Return": 69,"Mensaje":'Reserva creada correctamente'}, status = status.HTTP_201_CREATED)

        return Response({"Return":70,"Mensaje": reserva_serializer.errors}, status =status.HTTP_400_BAD_REQUEST)
        



@api_view(['GET', 'PUT','DELETE'])
def reserva_detail_api_view(request,pk=None):

    # consulta
    reserva = Reserva.objects.filter(id=pk).first()

    # validacion
    if reserva:

        # retrieve
        if request.method == 'GET':            
            reserva_serializer = ReservaSerializer(reserva)
            return Response(reserva_serializer.data, status = status.HTTP_200_OK)

        #actualizar
        elif request.method == 'PUT':           
            reserva_serializer =ReservaSerializer(reserva, data =request.data)
            if reserva_serializer.is_valid():
                reserva_serializer.save()
                return Response({"Return": 69,"Mensaje":'Reserva modificada correctamente.'}, status = status.HTTP_200_OK)
            return Response({"Return":70,"Mensaje": reserva_serializer.errors}, status =status.HTTP_400_BAD_REQUEST)
 
        # eliminar
        elif request.method == 'DELETE':            
            reserva.delete()
            return Response({"Return": 69,"Mensaje":'Reserva eliminada correctamente!'}, status = status.HTTP_200_OK)

    return Response({"Return":70,"Mensaje":'No se ha encontrado una reserva con estos datos'}, status = status.HTTP_400_BAD_REQUEST)


class PagoAPIView(APIView):

    def get(self, request): 
        
        pagos = Pago.objects.all()
        pagos_serializer = PagoSerializer(pagos, many = True)
        return Response(pagos_serializer.data)

    def post(self, request):

        data = request.data

        serializer = PagoSerializer(data = request.data)

        if serializer.is_valid():                      

            data_valida = serializer.validated_data

            pago_nuevo = Pago.objects.create(**data_valida)
        
            data = PagoSerializer(pago_nuevo).data  

            return Response({"Return": 69,"Mensaje": "El pago ha sido creado correctamente."})
          
        else:

            data = {'error': str(serializer.errors)}

        return Response(data = data)
    

class PagoListAPIView(APIView):

    def get(self, request, pk):

        pago= Pago.objects.get(id = pk)
        pago_serializer = PagoSerializer(pago)

        return Response(pago_serializer.data)

    def delete(self, request, pk):

        pago = Pago.objects.filter(id = pk)

        pago.delete()

        return Response({"Return": 69,"Mensaje": "Se eliminó el pago correctamente."})

class PDF(APIView):

    def post (request):

        reserva_serializer = ReservaSerializer(data=request.data)

        input = reserva_serializer.data

        build_direction = "LEFT_TO_RIGHT"

        table_attributes = {"style" : "width:100%"}

        json_to_html = convert(input, build_direction=build_direction, table_attributes=table_attributes)

        config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

        pdf = pdfkit.from_string(json_to_html, configuration=config)

        response = HttpResponse(pdf, content_type='application/pdf')

        response['Content-Disposition'] = 'attachment; filename="reserva.pdf" '

        return Response