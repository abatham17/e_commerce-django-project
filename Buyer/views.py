import email
from lib2to3.pgen2 import token
from msilib.schema import Class
from multiprocessing import context
from django.shortcuts import render
from .models import Customer
from django.contrib.auth import authenticate

# api libs
from rest_framework import status 
from rest_framework.response import Response
from Buyer import serializers
from rest_framework.decorators import APIView,api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

#import token
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

# @api_view(['GET','POST'])
# def add_new_buyer(request): 
#     if request.method == 'POST':
#        data=request.data
#        buy=Buyer_Info()
#        buy.First_Name=data['First_Name']
#        buy.Last_Name=data['Last_Name']
#        buy.Email=data['Email']
#        buy.Password=data['Password']
#        buy.save()
#        return Response({'msg':'buyer add'})
#     else:
#        return Response({'msg':'add buyer','format':{
#         "First_Name": "First name of a buyer",
#         "Last_Name": "last Name of a Buyer",
#         "Email": "email_id",
#         "Password": "Password"
#  }})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# class add_new_buyer(generics.CreateAPIView):
#    queryset=Buyer_Info
#    serializer_class=serializers.BuyerSerializer

# class update_buyer(generics.RetrieveUpdateDestroyAPIView):
#    queryset=Buyer_Info
#    serializer_class=serializers.BuyerSerializer

# class views_all_buyer(generics.ListAPIView):
#    queryset=Buyer_Info.objects.all()
#    serializer_class=serializers.BuyerSerializer

# class CustomerRegistration(APIView):
#    def post(self,request,format=None):
#       serializer=serializers.CustomerRegistrationSerializer(data=request.data)
#       if serializer.is_valid(raise_exception=True):
#          user=serializer.save()
#          return Response({'msg':'Registration Success'},status=status.HTTP_201_CREATED )
#       return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
   
class CustomerRegistration(generics.CreateAPIView):
   queryset=Customer
   serializer_class=serializers.CustomerRegistrationSerializer

class CustomerLoginView(APIView):
   def post(self,request,format=None):
      serializer=serializers.CustomerloginSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
         email=serializer.data.get('email')
         password=serializer.data.get('password')
         user=authenticate(email=email,password=password)
         if user is not None:
            token=get_tokens_for_user(user)
            return Response({"Token":token,'mag':'Login Success'},status=status.HTTP_200_OK)
         else:
            return Response({'errors':{'non_field_errors':['Email or password is not Valid']}},status=status.HTTP_404_NOT_FOUND)


class CustomerProfileView(APIView):
   permission_classes=[IsAuthenticated]
   def get(self,request,format=None):
      serializer=serializers.CustomerProfileView(request.user)
      return Response(serializer.data,status=status.HTTP_200_OK)

class CustomerChangePassword(APIView):
   permission_classes=[IsAuthenticated]
   def post(self,request,format=None):
      serializer=serializers.CustomerChangePasswordSerializer(data=request.data, context={'user':request.user})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Changed Successfully'},status=status.HTTP_200_OK)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SendPasswordRestEmailView(APIView):
   def post(self,request,format=None):
      serializer=serializers.SendPasswordRestEmailSerializer(data=request.data)
      if serializer.is_valid(raise_exception=True):
           return Response({'mag':'we send a Reset password link on your email'})
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CustomerPasswordResetView(APIView):
   def post(self,request,uid,token,format=None):
      serializer=serializers.CustomerPasswordRestSerializer(data=request.data, context={'uid':uid,'token':token})
      if serializer.is_valid(raise_exception=True):
         return Response({'msg':'Password Reset Successfully'},status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


