from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status

<<<<<<< HEAD
from icarusProjectApp.models import (

    Vuelo,
    Ciudad,
    Avion,
)

from icarusProjectApp.serializers import (

    VueloSerializer,
    CiudadSerializer,
    VueloCustomSerializer,
    CiudadCustomSerializer,
    AvionSerializer,
    AvionCustomSerializer,

)

class VueloAPIView(APIView):

    def get(self, request): 
        
        vuelos = Vuelo.objects.all()
        vuelos_serializer = VueloSerializer(vuelos, many = True)
        return Response(vuelos_serializer.data)

    def post(self, request):

        data = request.data

        if (VueloCustomSerializer.validando_vuelo(data) and VueloCustomSerializer.validando_ciudad(data) and VueloCustomSerializer.validando_avion_asociado(data)):
        
            serializer = VueloCustomSerializer(data)

            if serializer.is_valid():                      

                data_valida = serializer.validated_data
                            
                data_valida["id_ciudad_origen"] = Ciudad.objects.get(id = data_valida["id_ciudad_origen"])
                data_valida["id_ciudad_destino"] = Ciudad.objects.get(id = data_valida["id_ciudad_destino"])
                data_valida["id_avion_asociado"] = Avion.objects.get(id = data_valida["id_avion_asociado"])
                
                vuelo_nuevo = Vuelo.objects.create(**data_valida)
        
                data = VueloSerializer(vuelo_nuevo).data            

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

                return Response({"Success": "El vuelo ha sido editado correctamente."})

            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        else:
            data = {'error': str(serializer.errors)}

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

        return Response(data = data)

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

        return Response(data = data)
=======
>>>>>>> USER-001-002
