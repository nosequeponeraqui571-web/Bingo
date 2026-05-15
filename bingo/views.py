from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from .models import Jugador, TipoJugador
from django.contrib.auth import logout

# Create your views here.
def holamundo(request):
  return render(request, 'inicio.html')

def registro_jugador(request):
  tipos_disponibles = TipoJugador.objects.all()
  if request.method == 'POST':
    formulario = UserCreationForm(request.POST)
    eleccion_tipo_id = request.POST.get('tipo_jugador')
    if formulario.is_valid():
      usuario_nuevo = formulario.save()
      tipo_objeto = TipoJugador.objects.get(id=eleccion_tipo_id)
      Jugador.objects.create(
        usuario=usuario_nuevo, 
        tipo=tipo_objeto,
        creditos=0
      )
      login(request, usuario_nuevo)
      return redirect('inicio')
  else:
    formulario = UserCreationForm()
  return render(request, 'registro.html', {
    'formulario': formulario,
    'tipos': tipos_disponibles
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
  return redirect('inicio') # Al salir, lo mandamos de vuelta al inicio
