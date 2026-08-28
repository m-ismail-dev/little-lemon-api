# (بسم الله الرحمن الرحيم)

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemViewSet)

urlpatterns = [
    path('api/', include((router.urls, 'LittleLemonAPI'))),
]