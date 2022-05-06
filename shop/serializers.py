from getpass import getuser
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        depth = 1


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password','firstname','lastname','email')
        # pass hide er jonno 
        extra_kwargs = {'password':{"write_only": True, 'required':True}} 
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['userprofile']

    def validate(self, attrs):
        attrs['userprofile'] = self.context['request'].user
        return attrs
    def to_representation(self, instance):
        response = super.to_repreesentation(instance)
        response['userprofile'] = UserSerializer(instance.userprofile).data
        return response

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart 
        fields = "__all__"

class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = "__all__"
        depth = 1

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        depth = 1
        