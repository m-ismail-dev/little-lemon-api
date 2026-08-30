# (بسم الله الرحمن الرحيم)

from rest_framework import serializers

from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']


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


class CartItemSerializer(serializers.ModelSerializer):
    menu_item = MenuItemSerializer()
    menu_item_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = models.CartItem
        fields = ['id', 'menu_item', 'menu_item_id', 'quantity', 'unit_price', 'price']
        read_only_fields = ['user', 'unit_price', 'price']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
