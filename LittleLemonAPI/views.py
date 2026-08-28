# (بسم الله الرحمن الرحيم)

from rest_framework import viewsets, permissions

from . import models, serializers

class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = models.MenuItem.objects.all()
    serializer_class = serializers.MenuItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
