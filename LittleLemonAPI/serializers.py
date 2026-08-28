# (بسم الله الرحمن الرحيم)

from rest_framework import serializers

from . import models


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['title', 'price', 'featured', 'category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['slug', 'title']
