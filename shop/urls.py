from __future__ import barry_as_FLUFL
from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register('category', CategoryView, basename="CategoryView")
router.register('mycart', MyCart, basename='mycart')
router.register('oldorders', OldOrder, basename='oldorder')

urlpatterns = [ 
    path('',include(router.urls)),
    path('product/', ProductView.as_view(), name='products'),
    path('product/<int:id>/', ProductView.as_view(), name='product'),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('userdataupdate/',UserDataUpdate.as_view(),name='udataupdate'),
    path('profileimageupdata/', ProfileImageUpdate.as_view(),name="upimg"),
    
]