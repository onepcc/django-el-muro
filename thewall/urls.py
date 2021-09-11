from django.urls import path
from . import views
urlpatterns = [
    path('wall', views.index),
    # path('registro', views.registro),
    # path('login', views.login),
    # path('logout', views.logout),
    # path('success', views.success)
]
