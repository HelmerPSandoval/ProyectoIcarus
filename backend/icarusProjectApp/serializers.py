from rest_framework import serializers

from icarusProjectApp.models import (

    Usuario,
    Vuelo,
    Ciudad,
    Avion,
)

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

