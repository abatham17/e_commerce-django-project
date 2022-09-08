from asyncore import write
from dataclasses import fields
import email
from msilib.schema import Class
from select import select
from tkinter.ttk import Style
from xml.dom import ValidationErr
from xml.parsers.expat import model
from rest_framework import serializers

from Buyer.utils import Util
from .models import Customer
from rest_framework.response import Response
from django.contrib.auth import authenticate

#incodeing lib

from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
#genrate token class
from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# class BuyerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Buyer_Info
#         fields='__all__'

class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}
    ,write_only=True)
    class Meta:
        model=Customer
        fields=['email','name','password','password2','contact', 'seller','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and confirm password dosen't match")
        return attrs
    
    def create(self, validated_data):
        user=Customer.objects.create_user(**validated_data)
        token=get_tokens_for_user(user)
        raise serializers.ValidationError({'Token':token,'msg':'Registration Success'})

class CustomerloginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=Customer
        fields=['email','password']

class CustomerProfileView(serializers.ModelSerializer):
    class Meta:
        model=Customer
        fields=['id','email','name','contact','seller'] 

class CustomerChangePasswordSerializer(serializers.Serializer):
      old_password=serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
      password = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
      password2 = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
      class Meta:
        fields=['old_password','password','password2']
      def validate(self, attrs):
        old_password=attrs.get('old_password')
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        ol_pass=authenticate(email=user,password=old_password)
        if ol_pass is not None:
            if password !=password2:
                raise serializers.ValidationError("Password and confirm Password dosen't match")
            user.set_password(password)
            user.save()
            return attrs
        else:
            raise serializers.ValidationError("Old password dose not match")
        

class SendPasswordRestEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if Customer.objects.filter(email=email).exists():
            user=Customer.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('password reset token',token)
            link=' http://localhost:8000/rest-password/'+uid+'/'+token
            print('link',link)
            body='Click Here to Reset your Password'+link
            data={
                'email_subject':"Reset Your Password",
                 'body':body,
                 'to_email': user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise serializers.ValidationError('your are not a Registerd User')

class CustomerPasswordRestSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255,style={'input_type':'password'}, write_only=True)
    class Meta:
        fields=['password','password2']

    def validate(self, attrs):
        try:
           password=attrs.get('password')
           password2=attrs.get('password2')
           uid=self.context.get('uid')
           token=self.context.get('token')
           if password != password2:
                raise serializers.ValidationError("password and confirm password doesn't match")
           id=smart_str(urlsafe_base64_decode(uid))
           user=Customer.objects.get(id=id)
           if not PasswordResetTokenGenerator().check_token(user,token):
                raise serializers.ValidationError('Token is not valid or expired')
           user.set_password(password)
           user.save()
           return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise serializers.ValidationError("Token is not valid or expired")

            