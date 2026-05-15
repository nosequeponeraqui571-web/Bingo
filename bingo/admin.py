from django.contrib import admin

# Register your models here.
from .models import TipoSocio, Socio, Prestamo, TipoJugador, Jugador

# Register your models here.
admin.site.register(TipoSocio)
admin.site.register(Socio)
admin.site.register(Prestamo)
admin.site.register(TipoJugador)
admin.site.register(Jugador)