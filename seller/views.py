import email
from importlib.resources import contents
from itertools import product
from msilib.schema import Class
from multiprocessing import context
import re
from turtle import title
from urllib import request, response
from django.shortcuts import render
import json

from Buyer.models import Customer
from .models import product_det,Category,Cart,tag_pro
from seller import serializers
from .serializers import productSerializers
# api libs
from rest_framework import status 
from rest_framework.response import Response
from seller import serializers
from rest_framework.decorators import APIView,api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.

# @api_view(['GET','POST'])
# def add_product(request):
#     if request.method == 'POST':
#         data=request.data
#         file=request.FILES
#         pro=product_det()
#         pro.Product_Name=data['Product_Name']
#         if len(request.FILES) !=0:
#             pro.Product_image=file['Product_image']
#         pro.seller_id=data['seller_id']
#         pro.Total_quantity=data['Total_quantity']
#         pro.save()
#         return Response({'msg':'Product added'})
#     else:    
#         return Response({"msg":'add your products',"Formet":{
#                 "Product_image": "Image of product",
#                 "Product_Name": "Name of product",
#                 "seller_id": "Seller_id",
#                 "Total_quantity": "Quantity",
#             }})

# @api_view(['GET'])
# def search_product(request,pn):
#     try:
#         pro=product_det.objects.get(Product_Name=pn)
#     except:
#         return Response({'msg':'product not found'})
#     if request.method == 'GET':
#         serializer=serializers.productSerializers(pro)
#         return Response(serializer.data)
    

# @api_view(['GET','POST'])
# def add_product(request):
#     if request.method=='POST':
#         data=request.FILE
#         print(data)
#         return Response({'msg':'Product added'})
#     else:    
#         return Response({"msg":'add your products',"Formet":{
#                 "Product_image": "Image of product",
#                 "Product_Name": "Name of product",
#                 "seller_id": "Seller_id",
#                 "Total_quantity": "Quantity",
#             }})

# class View_all_product(generics.ListAPIView):
#     queryset=product_det.objects.all()
#     serializer_class=productSerializers

class Add_product(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=serializers.productSerializers(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Product add Suessfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class view_all_product(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        chkseller=Customer.objects.filter(email=str(request.user))
        if chkseller.exists():
            valchk=chkseller.values()
            if valchk[0]['seller']!=False:
                get_product=product_det.objects.all().filter(seller_id=valchk[0]['id'])
                serializer=serializers.view_selers_product_serilizer(get_product, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response({'mag':'me be you are not registered or your not seller profile'},status=status.HTTP_404_NOT_FOUND)
        return Response({'msg':"you'r not registerd user"},status=status.HTTP_400_BAD_REQUEST)

class search_product(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,qu,format=None):
        chk_Search_id=Customer.objects.filter(email=request.user)
        if chk_Search_id.exists():
            chl_seller=chk_Search_id.values()
            if chl_seller[0]['seller']!=True:
                get_product=product_det.objects.all().filter(Product_Name=qu)
                serializer=serializers.search_product_serilizer(get_product,many=True)
                return Response(serializer.data)
            return Response({'msg':'you are seller profile'},status=status.HTTP_401_UNAUTHORIZED)
        return Response({'msg':'Your not a registerd user plz registerd your self'},status=status.HTTP_404_NOT_FOUND)

    
class add_Category(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=serializers.add_categody_serialiser(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Category add Suessfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class list_of_product_by_Categeory(APIView):
   permission_classes=[IsAuthenticated]
   def get(self,request,que,format=None):
    filter_Cate_id=Category.objects.filter(title=que).values()
    fetch_all_products=product_det.objects.all().filter(Category_id=filter_Cate_id[0]['id'])
    serializer=serializers.list_of_product_by_Categeory_serializer(fetch_all_products,many=True)
    return Response(serializer.data)

class Category_list(generics.ListAPIView):
    permission_classes=[IsAuthenticated]
    queryset=Category.objects.all()
    serializer_class=serializers.Categeory_listing
    
class add_cart(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,pid,format=None):
        fetch_pro=product_det.objects.get(id=pid)
        fetch_Coustmer=Customer.objects.get(email=str(request.user))
        chk_avi_pro=Cart.objects.filter(Customer_id_id=fetch_Coustmer,product_id_id=fetch_pro)
        if chk_avi_pro.exists():
            return Response({'msg':'your Product all ready in the cart'},status=status.HTTP_406_NOT_ACCEPTABLE)
        ct=Cart()
        ct.product_id=fetch_pro
        ct.Customer_id=fetch_Coustmer
        ct.save()
        return Response({'msg':'successfully add to cart'},status=status.HTTP_202_ACCEPTED)

class listing_of_cart(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,format=None):
        fetch_customer=Customer.objects.filter(email=str(request.user))
        if fetch_customer.exists():
            Cust_val=fetch_customer.values()
            if Cust_val[0]['seller']!=True:
                fetch_carts=Cart.objects.all().filter(Customer_id_id=Cust_val[0]['id']).values()
                if fetch_carts.exists():
                    product_id_list=[]
                    for i in fetch_carts:
                        product_id_list.append(i['product_id_id'])
                    serializ_data=[]
                    for j in product_id_list:
                        fetch_product=product_det.objects.filter(id=j)
                        serializer=serializers.Cart_listing(fetch_product,many=True)
                        serializ_data.append(serializer.data)    
                    return Response(serializ_data,status=status.HTTP_200_OK)
                return Response({'msg':'the Cart is empty'},status=status.HTTP_204_NO_CONTENT)
            return Response({'msg':'your are not a buyers profile'},status=status.HTTP_401_UNAUTHORIZED)

class tag_products(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializer=serializers.tag_products(data=request.data,context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'tag add Suessfully'},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class listing_of_tages_products(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request,id,format=None):
        fetch_tags=tag_pro.objects.filter(product_id_id=id).values()
        if fetch_tags.exists():
            t_pro=fetch_tags[0]['t_products']
            jsonDec = json.decoder.JSONDecoder()
            tag_product_list = jsonDec.decode(t_pro)
            all_tag_pro=[]
            for i in tag_product_list:
                fetch_tags_products=product_det.objects.filter(id=i)
                serializer=serializers.tags_listing(fetch_tags_products,many=True)
                all_tag_pro.append(serializer.data)
            return Response(all_tag_pro,status=status.HTTP_200_OK)
        return Response({'msg':'taged product are not exists plz tag the product first'})  
            



