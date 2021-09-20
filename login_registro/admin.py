from django.contrib import admin
# TODO Se registran cada uno de los modelos que queremos usar en la app admin

from .models import User, Mensaje, Comentario
admin.site.register(User)
admin.site.register(Mensaje)
admin.site.register(Comentario)