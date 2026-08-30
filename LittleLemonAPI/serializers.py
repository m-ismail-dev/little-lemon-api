# (بسم الله الرحمن الرحيم)

from rest_framework import serializers

from . import models


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'slug', 'title']


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_title = serializers.SerializerMethodField()

    class Meta:
        model = models.OrderItem
        fields = ['id', 'menu_item', 'menu_item_title', 'quanity', 'unit_price', 'price']

    def get_menu_item_title(self, obj):
        return obj.menu_item.title


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
        read_only_fields = ['user', 'delivery_crew', 'order_items']
