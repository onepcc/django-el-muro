from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validador_basico(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        SOLO_LETRAS = re.compile(r'^[a-zA-Z. ]+$')

        errors = {}

        if len(postData['nombre']) < 2:
            errors['largo_nombre'] = "El nombre debe tener al menos 2 caracteres de largo";
        if len(postData['apellido']) < 2:
            errors['largo_apellido'] = "El apellido debe tener al menos 2 caracteres de largo";
        if len(postData['password']) < 8:
            errors['password'] = "La contraseña debe tener al menos 8 caracteres";

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "correo invalido"

         
        if postData['email'] != None:
            if self.filter(email=postData['email']).exists():
             errors['email_existe'] ='El email ya existe, registrese con otro email'
             print(errors)


        # if not SOLO_LETRAS.match(postData['name']):
        #     errors['solo_letras'] = "solo letras en nombreporfavor"


        if postData['password'] != postData['c_password'] :
            errors['password_confirm'] = "contraseña y confirmar contraseña no son iguales. "
            print("password no coinciden")
        
        return errors


class User(models.Model):
    CHOICES = (
        ("user", 'User'),
        ("admin", 'Admin')
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=70)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    #mensajes , todos los mensajes escritos por el usuario, user1.mensajes.all()
    #comentarios, todos los comentarios escritos por el usuario, user1.comentarios.all() 

    def __str__(self):
        return f"{self.firstname} {self.lastname}"
    
    def __repr__(self):
        return f"{self.firstname} {self.lastname}"


#THE WALL ##############################################################################
class Mensaje(models.Model):
    mensaje = models.TextField()
    user = models.ForeignKey(User, related_name="mensajes", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #comentarios , todos los comentarios hechos a un mensaje, mensaje1.comentarios.all()
    def __repr__(self):
            return f"<Usuario: {self.user.firstname},mensaje: {self.mensaje}, {self.updated_at}>"
    def __str__(self):
        return  f"Mensaje: {self.mensaje} de Usuario: {self.user.firstname}"

class Comentario(models.Model):
    user = models.ForeignKey(User, related_name="comentarios", on_delete = models.CASCADE)
    mensaje = models.ForeignKey(Mensaje, related_name="comentarios", on_delete = models.CASCADE)
    comentario = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __repr__(self):
            return f"Usuario: {self.user.firstname}, Mensaje: {self.mensaje.mensaje}, Comentario: {self.comentario}"
    def __str__(self):
            return f"Comentario: {self.comentario} de ({self.user.firstname}) a Mensaje: {self.mensaje.mensaje} de [{self.mensaje.user.firstname}] "
    