#app para que pueda ser consumida por la rest api

from rest_framework import serializers


from .models import Usuario, Reserva, Pago, Ciudad, Avion, Vuelo, Reserva_Vuelo



#serializers que definen la representacion de la api


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model =Usuario
        fields = '__all__'



class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model =Reserva
        fields = '__all__'



class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model =Pago
        fields = '__all__'

