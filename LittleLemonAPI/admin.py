from django.contrib import admin
from . import models
from django.contrib.auth.models import Group


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['slug', 'title']


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'featured', 'category']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'delivery_crew', 'status', 'date']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quanity', 'unit_price', 'price']


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu_item', 'quanity', 'unit_price', 'price']


# reregister new Group admin
admin.site.unregister(Group)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'num_members', 'num_perms']

    @admin.display(description='Number of members')
    def num_members(self, obj):
        return obj.user_set.count()

    @admin.display(description='Number of permissions')
    def num_perms(self, obj):
        return obj.permissions.all().count()
