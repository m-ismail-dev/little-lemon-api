# (بسم الله الرحمن الرحيم)

from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter(trailing_slash=False)
router.register('menu-items', views.MenuItemViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('api/', include((router.urls, 'LittleLemonAPI'))),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]
