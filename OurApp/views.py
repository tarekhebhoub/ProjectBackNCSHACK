from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework import generics
from django.shortcuts import get_object_or_404
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .gemini import AskGemini
# # Create your views here.

class SignUpView(generics.CreateAPIView):
    authentication_classes=()
    permission_classes=()
    serializer_class=serializers.UserSerializer
    def post(self,request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            user = models.User.objects.create_user(**serializer.validated_data)
            token=Token.objects.create(user=user)
            
            serializer = serializers.UserSerializer(user)
            data=serializer.data
            data["token"]=user.auth_token.key
            return Response(data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)




class LoginView(APIView):
    permission_classes=()
    serializer_class=serializers.LoginSerializer
    def post(self,request):
        username=request.data.get("username")
        password=request.data.get("password")
        user=authenticate(username=username,password=password)
        if user:
            # refresh = RefreshToken.for_user(user)
            try:
                Token.objects.create(user=user)
            except:
                Token.objects.filter(user=user).delete()
                Token.objects.create(user=user)
                
            return Response({
                "token":str(user.auth_token.key),
                "username":user.username,
                },status=status.HTTP_200_OK)
        else:
            return Response({"error":"Wrong Credentials"},status=status.HTTP_400_BAD_REQUEST)



#room=rapport it the like the medecale file of patient
class RoomView(APIView):
    def get(self,request):
        if request.user.is_client:
            rooms=models.Room.objects.all()
            serializer=serializers.RoomSerializer(rooms,many=True)
            return Response(serializer.data)
        else:
            return Response({'You are not client'})
    def post(self,request):
        data=request.data
        data['client']=request.user.id
        serializer = serializers.RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)



@api_view(['GET'])  # Use the appropriate HTTP method for your API
# @permission_classes([IsAuthenticated]) 
def RecommandDoctor(request):
    users=models.User.objects.filter(Specialite=request.data["sp"])
    serializer=serializers.UserSerializer(users,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def DemmandRendezVous(request):
    data=request.data
    data['client']=request.user.id
    serializer=serializers.RendezVousSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ListDesRendezVous(request):
    rendezVous=models.RendezVous.objects.filter(medecin=request.user.id)
    serializer=serializers.RendezVousSerializer(rendezVous,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def RpndrRendezVous(request):
    data1=request.data
    rendezVous=models.RendezVous.objects.get(id=data1["idRendezVous"])
    if data1["rpns"]=="yes":
        data={}
        data['medecin']=rendezVous.medecin.id
        data['client']=rendezVous.client.id
        data['rapport']=data1['roomId']
        # rapports=models.Rapport.objects.filter(client=rendezVous.client).order_by('created_at')
        # print(rapports.last().rapportText)
        # data['rapport']=rapports.last().id
        # data['date']=data1['date']
        serializer=serializers.MesPatiensSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            rendezVous.delete()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    rendezVous.delete()
    return Response({"Done"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def demandeAllRapport(request):
    data=request.data
    data['medecin']=request.user.id
    serializer=serializers.DemmandAllRapportsSerializer(data=data)
    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetDemmandAllRapport(request):
    Demmands=models.DemmandAllRapports.objects.filter(client=request.user.id)
    serializer=serializers.DemmandAllRapportsSerializer(Demmands,many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rpndrADemmandeAllRapport(request):
    data=request.data
    DemmandeAllR=models.DemmandAllRapports.objects.get(id=data["idDemmandeAllR"])
    if data["rpns"]=="yes":
        DemmandeAllR.canGetAllR=True
        DemmandeAllR.save()
    return Response({"Done"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllRapportByMedecin(request):
    DemmandeAllR = models.DemmandAllRapports.objects.get(client=request.data["idclient"], medecin=request.user.id)
    if DemmandeAllR.canGetAllR:
        rooms=models.Room.objects.filter(client=request.data['idclient'])
        serializer=serializers.RoomSerializer(rooms,many=True)
        return Response(serializer.data)
    return Response({"U don\'t Have acces to get all rapports"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def SendMsg(request):
    data=request.data
    reponse=AskGemini(data["question"])
    data["reponse"]=reponse
    print(data)
    serializer=serializers.MessageSerialize(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)





   
