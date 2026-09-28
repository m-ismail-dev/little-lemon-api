# (بسم الله الرحمن الرحيم)

from rest_framework import viewsets
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from . import models, serializers


User = get_user_model()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    queryset = models.CartItem.objects.all()
    serializer_class = serializers.CartItemSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = models.OrderItem.objects.all()
    serializer_class = serializers.OrderItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(groups__name='Managers')


class DeliveryCrewViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return User.objects.filter(groups__name='Delivery crew')
