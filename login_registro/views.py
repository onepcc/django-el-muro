from django.shortcuts import render, HttpResponse, redirect
from time import  localtime, strftime
from login_registro.models import *
from django.contrib import messages #para mensajes de validaciones
import bcrypt
from datetime import datetime, timedelta

def index(request):
    context = {
    'saludo': 'Hola'
    }
    return render(request, 'index.html', context)

def login(request):
    if request.method == 'GET':
        context = {
        'saludo': 'Hola'
        }
        return render(request, 'index.html', context)
    
    if request.method == 'POST':
        print(request.POST)

        usuarios= User.objects.filter(email=request.POST['email2'])
        if usuarios:
            usuario_sesion = usuarios[0]
            pass_db=usuario_sesion.password.encode()
            print(pass_db)

            if bcrypt.checkpw(request.POST['password2'].encode(), pass_db):
                print("password match")
                request.session['nombre']=usuario_sesion.firstname
                request.session['apellido']=usuario_sesion.lastname
                request.session['email']=request.POST['email2']
                request.session['id']=usuario_sesion.id
                messages.info(request,f"Bienvenido {request.session['nombre']}")
                
                # return redirect('/success')
                return redirect('/wall')
            else:
                print("failed password")
                messages.info(request,"Usuario no existe o password incorrecto")
                return redirect('/')
        else:
            print("failed password")
            messages.warning(request,"Usuario no existe o password incorrecto")
            return redirect('/')
             

def logout(request):
    if 'email' in request.session:
        del request.session['nombre']
        del request.session['apellido']
        del request.session['email']
        del request.session['id']
        
        
        messages.info(request,"Usuario deslogueado, hasta la proxima")

        context = {
        'saludo': 'Hola'
        }
        return redirect('/')



def registro(request):
    if request.method == 'GET':
            

            context = {
            'saludo': 'Hola'
            }
            return redirect('/')


    if request.method == 'POST':
        print(request.POST)

        errors = User.objects.validador_basico(request.POST)
        # compruebe si el diccionario de errores tiene algo en él
        if len(errors) > 0:
            # si el diccionario de errores contiene algo, recorra cada par clave-valor y cree un mensaje flash
            for key, value in errors.items():
                messages.error(request, value)

            #Guardamos en sesior para mantener datos en formulario en caso de errores
            request.session['nombre']=request.POST['nombre']
            request.session['apellido']=request.POST['apellido']
            request.session['email']=request.POST['email']
            request.session['pass']=request.POST['password']
            request.session['conf_pass']=request.POST['c_password']
            # redirigir al usuario al formulario para corregir los errores
            return redirect('/')
        
        else:
            # si el objeto de errores está vacío, eso significa que no hubo errores.
            # recuperar el blog para actualizarlo, realizar los cambios y guardar
            # leemos las variables del formulario
           
            request.session['nombre']=""
            request.session['apellido']=""
            request.session['email']=""
            request.session['pass']=""
            request.session['conf_pass']=""


            nombre_usuario= request.POST['nombre']
            apellido_usuario= request.POST['apellido']
            email= request.POST['email']
            passw= request.POST['password']
            c_password= request.POST['c_password']
                        
            # ejecutamos comando ORM para crear usuario, los campos deben coincidir con el modelo definido
            pass_hash= bcrypt.hashpw(passw.encode(), bcrypt.gensalt()).decode()
            print("Ecriptado", pass_hash)
            
            user_db = User.objects.create(
                firstname = nombre_usuario,
                lastname = apellido_usuario,
                email = email,
                password = pass_hash,
                
                )

            #Rescatamos el datos del usuario creado, para sesion
            request.session['id']=user_db.id
            request.session['nombre']=nombre_usuario
            request.session['apellido']=apellido_usuario
            request.session['email']=email
            
            messages.success(request, f"Usuario creado correctamente {nombre_usuario}")
            print("Usuario CREADO CORRECTAMENTEE!!!", user_db)
            
            return redirect('/wall')
            # return redirect('/success')



def success(request):
    if 'email' not in request.session:
        messages.error(request,"Solo usuarios logueados pueden ver esta pagina")
        print("*****SIM PERMISOS*******")  
        return redirect('/')
        
    else:
            
        context = {
        'saludo': 'Hola'
        
        }
        return render(request, 'success.html', context)

def wall(request):
    if 'email' not in request.session:
        messages.error(request,"Solo usuarios logueados pueden ver esta pagina")
        print("*****SIM PERMISOS*******")  
        return redirect('/')
        
    else:

        mensajes= Mensaje.objects.all()
# TODO hacer que el borrar solo salga dentro de 30min de creado el msg
        
        
        context = {
        'mensajes': mensajes,
        }
        return render(request, 'wall.html', context)


def mensaje(request):
    if request.method == 'POST':
        print(request.POST)

        usuario_mensaje=User.objects.get(id=request.POST['msg_usuario'])           
        mensaje_db = Mensaje.objects.create(
            user = usuario_mensaje,
            mensaje = request.POST['mensaje'],
                        
            )
        
        messages.success(request, f"Has realizado un Mensaje exitoso {request.session['nombre']}")
        print("Mensaje exitoso", mensaje_db)
        
        return redirect('/wall')

def borrar_msg(request,msg_id):
    msg_borrar = Mensaje.objects.get(id=msg_id)
    # ejecutamos comando ORM para BORRAR Mensaje, los campos deben coincidir con el modelo definido
    msg_borrar.delete()
    messages.error(request, "Se ha eliminado el mensaje ")

    return redirect('/wall')

def comentario(request):
    if request.method == 'POST':
        print(request.POST)

        mensaje_comentario=Mensaje.objects.get(id=request.POST['mensaje_id'])           
        usuario_comentario=User.objects.get(id=request.session['id'])    
        comentario_db = Comentario.objects.create(
            user = usuario_comentario,
            mensaje = mensaje_comentario,
            comentario= request.POST['comentario']
                        
            )
        

        messages.success(request, f"Has realizado un Comentario exitoso {request.session['nombre']}")
        print("Mensaje exitoso", comentario_db)
        
        return redirect('/wall')