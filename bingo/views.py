from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import Jugador

def holamundo(request):
    return render(request, 'inicio.html')

def registro_jugador(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario_nuevo = formulario.save()
            
            # Creamos el Jugador adaptado a tu NUEVO modelo de base de datos
            Jugador.objects.create(
                aliasjugador=usuario_nuevo.username,
                fecharegistrojugador=timezone.now(),
                saldocreditojugador=0.00,
                estadocuentajugador='Activo'
            )
            login(request, usuario_nuevo)
            return redirect('inicio')
    else:
        formulario = UserCreationForm()
        
    return render(request, 'registro.html', {
        'formulario': formulario
    })

def login_jugador(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            # Autentica y valida que los datos coincidan
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('inicio')
    else:
        formulario = AuthenticationForm()
    return render(request, 'login.html', {'formulario': formulario})

def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')