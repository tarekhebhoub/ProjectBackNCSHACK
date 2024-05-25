from rest_framework import serializers
from . import models
from django.contrib.auth import authenticate
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields=('first_name','last_name','username','password','Date_Of_Birth')
        extra_kwargs={'password':{'write_only':True}}



class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields=('username','password')



class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Room
        fields=('id','client')

class RendezVousSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.RendezVous
        fields=('id','client','medecin','pourcentage')


class MesPatiensSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.MesPatiens
        fields=('id','client','medecin','rapport','date')
    

class DemmandAllRapportsSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.DemmandAllRapports
        fields=('id','client','medecin')

class MessageSerialize(serializers.ModelSerializer):
    class Meta:
        model=models.Message
        fields=('id','room','question','reponse')