from rest_framework import generics, mixins, viewsets
from rest_framework.views import APIView
from .serializers import *

from .models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User

class ProductView(generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    ):
    queryset = Product.objects.all().order_by("-id")
    serializer_class = ProductSerializer
    lookup_field = 'id'

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

class CategoryView(viewsets.ViewSet):

    def list(self,request):
        queryset = Category.objects.all().order_by("-id")
        serializer = CategorySerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Category.objects.get(id=pk)
        serializer = CategorySerializer(queryset).data
        
        # browser e category er sathe oitar product o dekhate 
        all_data = []
        category_products = Product.objects.filter(category_id=serializer['id'])
        category_products_serializer = ProductSerializer(category_products,many=True)

        serializer['category_products']= category_products_serializer.data
        all_data.append(serializer)

        return Response(all_data)

class ProfileView(APIView):
    authentication_classes=[TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    def get(self,request):
        try:
            query = Profile.objects.get(userprofile=request.user)
            serializer = ProfileSerializer(query)
            response_message = {"error":False,"data":serializer.data}
        except:
            response_message = {"error":True,"message":"Somthing is Wrong"}
        return Response(response_message)


class UserDataUpdate(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [ IsAuthenticated, ]

    def post(self,request):
        try:
            user = request.user
            data = request.data
            
            user_obj = User.objects.get(username=user)
            user_obj.first_name = data['first_name']
            user_obj.last_name = data['last_name']
            user_obj.email = data['email']
            user_obj.save()

        except:
            response_msg = {"message": "user not updated"}
        return Response(response_msg)

class ProfileImageUpdate(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [ IsAuthenticated, ]

    def post(self,request):
        try:
            user = request.user
            queryset = Profile.objects.get(userprofile=user)
            data = request.data
            print(data)
            serializer = ProfileSerializer(queryset,data=data,context={"request": request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print(serializer)
            response_msg = {'message':'image updated successfully..'}
        except:
            response_msg = {'message':'not updated image'}
        return Response(response_msg)

class MyCart(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication,]

    def list(self,request):
        queryset = Cart.objects.filter(customer=request.user.profile)
        serializer = CartSerializer(queryset, many=True)
        all_data=[]
        for cart in serializer.data:
            cart_product = CartProduct.objects.filter(cart=cart['id'])
            cart_product_serializer = CartProductSerializer(CartProduct,many=True)
            cart['cart_product'] = CartProductSerializer.data
            all_data.append(cart)

        return Response(all_data)

class OldOrder(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication,]

    def list(self,request):
        queryset = Order.objects.filter(cart__customer=request.user.profile)
        print(queryset)
        serializer = OrderSerializer(queryset,many=True)

        all_data = []
        for order in serializer.data:
            cart_product = CartProduct.objects.filter(cart_id = order['cart']['id'])
            cart_product_serializer = CartProductSerializer(cart_product,many=True)
            order['cart_product'] = cart_product_serializer.data
            all_data.append(order)
        return Response(all_data)

    def retrieve(self,request,pk=None):
        try:
            query = Order.objects.get(id=pk)
            serializer = OrderSerializer(query)
            all_data = []
            cartproduct = CartProduct.objects.filter(cart_id=serializer.data['cart']['id'])
            cartproduct_serializer = CartProductSerializer(cartproduct,many=True)
            serializer.data['cartproduct'] = cartproduct_serializer.data
            all_data.append(serializer.data)
            response_msg = {'error': False, 'data':all_data}
        except:
            response_msg = {'error': True, 'message':'not found'}

        return Response(response_msg)
    
# class AddToCart()