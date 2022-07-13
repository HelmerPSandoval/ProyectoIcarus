# DJANGO REST framework
from turtle import pd
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
import json
#import pdfkit
from json2table import convert
from fpdf import FPDF
from django.http import HttpResponse

from http import server
import smtplib
import os
from email.message import EmailMessage

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

class PDF(FPDF):
    pass

    def logo(self, name, x, y, w, h):
        self.image(name, x, y, w, h)
    
    def titles(self, title):
        self.set_xy(0.0,0.0)
        self.set_font('Arial', 'B', 16)
        self.cell(w=210.0, h=40.0, align='C', txt=title, border=0)
    

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

            rut_usuario = reserva_serializer.data['rut_usuario']

            email_usuario = Usuario.objects.values_list('email', flat=True).get(rut=rut_usuario)

            input = reserva_serializer.data
            id = json.dumps(input['id'])
            fecha_reserva = json.dumps(input['fecha_reserva'])
            fecha_reserva= re.sub('"','',fecha_reserva)
            valor_reserva = json.dumps(input['valor_reserva'])
            vuelo = json.dumps(input['vuelo'])
            rut_usuario = json.dumps(input['rut_usuario'])
            rut_usuario= re.sub('"','',rut_usuario)



            pdf = PDF()
            pdf.add_page()
            pdf.logo("IcarusAirline.png", 0, 0, 60, 15)
            pdf.set_text_color(0,0,0)
            pdf.titles("Comprobante de reserva")
            pdf.ln()
            pdf.cell(7,7,"Este es el comprobante generado luego de la reserva realizada en Icarus")
            pdf.ln()
            pdf.cell(7,7,"Airlines. A continuación, se muestran los datos referente a la reserva:")
            pdf.ln()
            pdf.ln()
            pdf.cell(10,10,"- Rut del cliente: " + rut_usuario)
            pdf.ln()
            pdf.cell(10,10,"- Codigo de reserva: " + id)
            pdf.ln()
            pdf.cell(10,10,"- Fecha de reserva: " + fecha_reserva)
            pdf.ln()
            pdf.cell(10,10,"- Valor de la reserva: " + valor_reserva)
            pdf.ln()
            pdf.cell(10,10,"- Vuelo designado: " + vuelo)
            for i in range(15):
                pdf.ln()
            pdf.set_text_color(255,0,0)
            pdf.cell(7,7,"En caso de que tenga alguna inquietud o usted no haya realizado dicha ")
            pdf.ln()
            pdf.cell(7,7,"reserva, por favor contactarnos a través del siguiente correo electrónico:")
            pdf.ln()
            pdf.cell(7,7,"icarusairline.contact@gmail.com")
            pdf.set_author("Icarus Airline S.A")
            pdf.output("comprobante_de_reserva.pdf", "F")
           

            msg = EmailMessage()

            msg['Subject'] = 'Comprobante de reserva'

            msg['From'] = 'Icarus Airlines'

            msg['To'] = email_usuario

            msg.set_content("Comprobante de reserva")

            filepath = os.path.join("C:/Users/OMEN/Desktop/Universidad/ProyectoSoftware/ProyectoIcarus/backend" , "comprobante_de_reserva.pdf")
            #filepath = os.path.join("C:\\Users\\miste\\Desktop\\correos icarus", "comprobante.pdf")

            with open(filepath, 'rb') as comprobante:

                archivo_adjunto = comprobante.read()

                file_name = 'comprobante_de_reserva.pdf' 

                msg.add_attachment(archivo_adjunto, maintype = "aplication", subtype = "pdf",filename = file_name)

            server = smtplib.SMTP_SSL('smtp.gmail.com',465)

            server.login('icarusairline.noreply@gmail.com','xzgfaiusjuroclyt')

            server.send_message(msg)

            server.quit()  
           
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

