from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Jugador, Carton, PartidaBingo, Bingo
from .utils import generar_matriz_bingo, generar_codigo_unico
import json
def holamundo(request):
    # Obtenemos los bingos que no estén cancelados ni finalizados
    bingos = Bingo.objects.exclude(estadobingo__in=['Cancelado', 'Finalizado'])
    return render(request, 'inicio.html', {'bingos': bingos})

def registro_jugador(request):
    if request.method == 'POST':
        formulario = UserCreationForm(request.POST)
        if formulario.is_valid():
            usuario_nuevo = formulario.save()
            
            # Creamos el Jugador en la base de datos
            Jugador.objects.create(
                aliasjugador=usuario_nuevo.username,
                fecharegistrojugador=timezone.now(),
                saldocreditojugador=0.00,
                estadocuentajugador='Activo'
            )
            login(request, usuario_nuevo)
            messages.success(request, f'¡Bienvenido {usuario_nuevo.username}! Tu cuenta ha sido creada.')
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
            usuario = formulario.get_user()
            login(request, usuario)
            messages.success(request, f'¡Hola de nuevo, {usuario.username}!')
            return redirect('inicio')
    else:
        formulario = AuthenticationForm()
    return render(request, 'login.html', {'formulario': formulario})

def cerrar_sesion(request):
    logout(request)
    messages.info(request, 'Has cerrado tu sesión exitosamente.')
    return redirect('inicio')

@login_required
def comprar_carton(request, bingo_id):
    """
    Procesa la compra del cartón desde el formulario HTML
    """
    if request.method == 'POST':
        try:
            # Buscamos al jugador que está logueado
            jugador = Jugador.objects.get(aliasjugador=request.user.username)
            
            # Buscamos el bingo que se quiere jugar
            bingo = get_object_or_404(Bingo, idbingo=bingo_id)
            
            # Buscamos la primera partida asociada a este bingo
            partida = PartidaBingo.objects.filter(idbingo=bingo).first()
            
            if not partida:
                messages.error(request, 'Este bingo aún no tiene una partida activa configurada.')
                return redirect('inicio')
            
            # --- Aquí podrías validar saldo ---
            # if jugador.saldocreditojugador < bingo.preciocarton:
            #     messages.error(request, 'No tienes saldo suficiente.')
            #     return redirect('inicio')
            
            # Generamos el cartón matemático
            matriz_json = generar_matriz_bingo()
            codigo = generar_codigo_unico()
            
            # Guardamos en la base de datos
            Carton.objects.create(
                idjugador=jugador,
                idpartida=partida,
                codigocarton=codigo,
                matriznumeros=matriz_json,
                preciopagado=bingo.preciocarton,
                fechacompra=timezone.now(),
                estadocarton='Disponible'
            )
            
            # Redirigimos al inicio con un mensaje verde de éxito
            messages.success(request, f'¡Cartón N° {codigo} comprado con éxito para el {bingo.titulobingo}!')
            
        except Jugador.DoesNotExist:
            messages.error(request, 'Error: No se encontró un perfil de jugador asociado a tu usuario.')
        except Exception as e:
            messages.error(request, f'Error al generar el cartón: {str(e)}')
            
    return redirect('inicio')

@login_required
def mis_cartones(request):
    """
    Vista para que el jugador vea los cartones que ha comprado.
    """
    try:
        jugador = Jugador.objects.get(aliasjugador=request.user.username)
        # Traemos los cartones del jugador, los más recientes primero
        cartones_db = Carton.objects.filter(idjugador=jugador).order_by('-fechacompra')
        
        cartones_procesados = []
        for carton in cartones_db:
            # Transformamos la matriz string que guardamos en la BD de vuelta a una lista de Python
            matriz = json.loads(carton.matriznumeros)
            
            # Recopilamos datos amigables para el HTML
            cartones_procesados.append({
                'codigo': carton.codigocarton,
                'bingo_titulo': carton.idpartida.idbingo.titulobingo if carton.idpartida else 'Bingo General',
                'matriz': matriz,
                'fecha': carton.fechacompra
            })
            
    except Jugador.DoesNotExist:
        cartones_procesados = []
        
    return render(request, 'mis_cartones.html', {'cartones': cartones_procesados})