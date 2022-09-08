from dataclasses import fields
import email
from locale import currency
from pyexpat import model
from re import search
from unittest.util import _MAX_LENGTH
from urllib import request
from wsgiref import validate
from rest_framework import serializers

from Buyer.models import Customer
from .models import product_det,Category,tag_pro
from dataclasses import fields
from rest_framework import status 

class productSerializers(serializers.Serializer):
       Product_image=serializers.ImageField(max_length=None, use_url=True)   
       Product_Name=serializers.CharField(max_length=30)
       Total_quantity=serializers.IntegerField()
       price=serializers.DecimalField(max_digits=50, decimal_places=2)
       category=serializers.CharField(max_length=100)
       currency_type=serializers.CharField(max_length=10)
       active=serializers.BooleanField(allow_null=True, required=False)
       class Meta:
        fields=['Product_image','Product_Name','Total_quantity','price','category','currency_type','active']
       def validate(self, attrs):
            Product_image=attrs.get('Product_image')
            Product_Name=attrs.get('Product_Name')
            Total_quantity=attrs.get('Total_quantity')
            price=attrs.get('price')
            category=attrs.get('category')
            currency_type=attrs.get('currency_type')
            active=attrs.get('active')
            user=self.context.get('user')
            Cate=Category.objects.all().values()
            Catel=[]
            for i in Cate:
                Catel.append(i['title'])
            chkuser=Customer.objects.filter(email=user)
            if chkuser.exists():
                fetch_det=chkuser.values()
                if fetch_det[0]['seller']!=False:
                    chkCate=Category.objects.filter(title=category)
                    if chkCate.exists():
                        if currency_type == 'USD' or currency_type == 'INR':
                            if Total_quantity == 0 and active == True:
                                    raise serializers.ValidationError('Your quantity is zero your product activaion should be false') 
                            getCate=Category.objects.get(title=category)
                            get_user=Customer.objects.get(email=user)
                            pro=product_det()
                            pro.Product_image=Product_image
                            pro.Product_Name=Product_Name
                            pro.seller_id=fetch_det[0]['id']
                            pro.Total_quantity=Total_quantity
                            pro.user=get_user
                            pro.price=price
                            pro.currency_type=currency_type
                            pro.Category=getCate
                            pro.save()
                            return attrs
                        raise serializers.ValidationError({'the currenty type available only':['USD','INR']})
                    raise serializers.ValidationError({'the Category you selected is not available the available Categorys are':Catel})
                raise serializers.ValidationError('your not seller profile')


class search_product_serilizer(serializers.ModelSerializer):
    class Meta:
        model=product_det
        fields= ['id','Product_image','Product_Name','Total_quantity','date','price','currency_type']


class view_selers_product_serilizer(serializers.ModelSerializer):
    class Meta:
        model=product_det
        fields=['Product_image','Product_Name','Total_quantity','price','date','time']
    

class add_categody_serialiser(serializers.Serializer):
    title=serializers.CharField(max_length=255)
    class Meta:
        fields=['title']
    def validate(self, attrs):
        title=attrs.get('title')
        user=self.context.get('user')
        chk_user=Customer.objects.filter(email=user)
        if chk_user.exists():
            chk_seller=chk_user.values()
            if chk_seller[0]['seller']!=False:
                chk_category=Category.objects.filter(title=title)
                if chk_category.exists():
                    raise serializers.ValidationError('this Category is alreay exist')
                cate=Category()
                cate.title=title
                cate.save()
                return attrs
            raise serializers.ValidationError('Your are Customer Profile you can not add Category')
        raise serializers.ValidationError('Your not register person to add Category plz register your self first')


class list_of_product_by_Categeory_serializer(serializers.ModelSerializer):
    class Meta:
        model=product_det
        fields='__all__'
    
class Categeory_listing(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class Cart_listing(serializers.ModelSerializer):
    class Meta:
        model=product_det
        fields='__all__'

class tag_products(serializers.Serializer):
    product_id=serializers.IntegerField()
    tag_product_1_id=serializers.IntegerField(required=False)
    tag_product_2_id=serializers.IntegerField(required=False)
    tag_product_3_id=serializers.IntegerField(required=False)
    tag_product_4_id=serializers.IntegerField(required=False)
    tag_product_5_id=serializers.IntegerField(required=False)
    class Meta:
        fields=['product_id','tag_product_1_id','tag_product_2_id','tag_product_3_id','tag_product_4_id','tag_product_5_id']
    def validate(self, attrs):
        pro_id=attrs.get('product_id')
        tag_product_1_id=attrs.get('tag_product_1_id')
        tag_product_2_id=attrs.get('tag_product_2_id')
        tag_product_3_id=attrs.get('tag_product_3_id')
        tag_product_4_id=attrs.get('tag_product_4_id')
        tag_product_5_id=attrs.get('tag_product_5_id')
        user=self.context.get('user')
        fetch_user=Customer.objects.filter(email=user)
        if fetch_user.exists():
            fetch_user_value=fetch_user.values()
            if fetch_user_value[0]['seller']==True:
                chk_pro=tag_pro.objects.filter(product_id_id=pro_id)
                if chk_pro.exists():
                    raise serializers.ValidationError("you all ready tag that product")
                if tag_product_5_id != None and tag_product_4_id != None and tag_product_3_id != None and tag_product_2_id != None and tag_product_1_id != None:
                    pid=product_det.objects.get(id=pro_id)
                    tags=[tag_product_1_id,tag_product_2_id,tag_product_3_id,tag_product_4_id,tag_product_5_id] 
                    tagp=tag_pro()
                    tagp.t_products=tags
                    tagp.product_id=pid
                    tagp.save()
                    return attrs
                elif tag_product_5_id == None and tag_product_4_id != None and tag_product_3_id != None and tag_product_2_id != None and tag_product_1_id != None:
                    pid=product_det.objects.get(id=pro_id)
                    tags=[tag_product_1_id,tag_product_2_id,tag_product_3_id,tag_product_4_id] 
                    tagp=tag_pro()
                    tagp.t_products=tags
                    tagp.product_id=pid
                    tagp.save()
                    return attrs
                elif tag_product_5_id == None and tag_product_4_id == None and tag_product_3_id != None and tag_product_2_id != None and tag_product_1_id != None:
                    pid=product_det.objects.get(id=pro_id)
                    tags=[tag_product_1_id,tag_product_2_id,tag_product_3_id] 
                    tagp=tag_pro()
                    tagp.t_products=tags
                    tagp.product_id=pid
                    tagp.save()
                    return attrs
                elif tag_product_5_id == None and tag_product_4_id == None and tag_product_3_id == None and tag_product_2_id != None and tag_product_1_id != None:
                    pid=product_det.objects.get(id=pro_id)
                    tags=[tag_product_1_id,tag_product_2_id] 
                    tagp=tag_pro()
                    tagp.t_products=tags
                    tagp.product_id=pid
                    tagp.save()
                    return attrs
                elif tag_product_5_id == None and tag_product_4_id == None and tag_product_3_id == None and tag_product_2_id == None and tag_product_1_id != None:
                    pid=product_det.objects.get(id=pro_id)
                    tags=[tag_product_1_id] 
                    tagp=tag_pro()
                    tagp.t_products=tags
                    tagp.product_id=pid
                    tagp.save()
                    return attrs
                elif tag_product_5_id == None and tag_product_4_id == None and tag_product_3_id == None and tag_product_2_id == None and tag_product_1_id == None:
                    raise serializers.ValidationError('at least one product should be taged')
            raise serializers.ValidationError('your not a seller profile')
        raise serializers.ValidationError('you are not a registered user')    

class tags_listing(serializers.ModelSerializer):
    class Meta:
        model=product_det
        fields='__all__'