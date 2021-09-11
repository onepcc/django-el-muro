from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registro', views.registro),
    path('login', views.login),
    path('logout', views.logout),
    path('success', views.success),
    path('wall', views.wall),
    path('mensaje', views.mensaje),
    path('borrar_msg/<int:msg_id>', views.borrar_msg),
    path('comentario', views.comentario),
]
