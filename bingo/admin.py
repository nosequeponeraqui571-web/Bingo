from django.contrib import admin
from .models import (
    TipoSocio, Socio, CuentaBancaria, MetodoPago, 
    Prestamo, Pago, Bingo, Ahorro, 
    Jugador, Carton, PlataformaJuego, SesionJuego, 
    Regalo, AporteSemanal, PartidaBingo
)

# ==========================================
# IMAGEN 1: Socios
# ==========================================
@admin.register(TipoSocio)
class TipoSocioAdmin(admin.ModelAdmin):
    list_display = ('idtiposocio', 'nombretiposocio', 'roltiposocio')
    search_fields = ('nombretiposocio', 'roltiposocio')

@admin.register(Socio)
class SocioAdmin(admin.ModelAdmin):
    list_display = ('cisocio', 'primernombresocio', 'primerapellidosocio', 'idtiposocio', 'estadosocio')
    list_filter = ('estadosocio', 'sexosocio', 'idtiposocio')
    search_fields = ('cisocio', 'primernombresocio', 'primerapellidosocio')

# ==========================================
# IMAGEN 2: Cuentas y Pagos
# ==========================================
@admin.register(CuentaBancaria)
class CuentaBancariaAdmin(admin.ModelAdmin):
    list_display = ('numerocuenta', 'nombrebanco', 'idsocio', 'tipocuenta', 'esprincipal', 'estadocuenta')
    list_filter = ('estadocuenta', 'esprincipal', 'tipocuenta')
    search_fields = ('numerocuenta', 'nombrebanco')

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('nombremetodopago', 'estadometodopago')
    list_filter = ('estadometodopago',)

# ==========================================
# IMAGEN 3: Préstamos
# ==========================================
@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = ('idprestamo', 'idsocio', 'montoprestamosolicitado', 'saldopendiente', 'estadoprestamo', 'fechavencimiento')
    list_filter = ('estadoprestamo',)
    search_fields = ('idsocio__primernombresocio', 'idsocio__primerapellidosocio')

@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ('idpago', 'idprestamo', 'montopagado', 'fechapago', 'estadopago')
    list_filter = ('estadopago', 'fechapago')
    search_fields = ('numeroreferencia',)

# ==========================================
# IMAGEN 4: Bingo y Ahorros
# ==========================================
@admin.register(Bingo)
class BingoAdmin(admin.ModelAdmin):
    list_display = ('titulobingo', 'fechaprogramadabingo', 'tipobingo', 'preciocarton', 'premiomayor', 'estadobingo')
    list_filter = ('estadobingo', 'tipobingo', 'fechaprogramadabingo')
    search_fields = ('titulobingo',)

@admin.register(Ahorro)
class AhorroAdmin(admin.ModelAdmin):
    list_display = ('idahorro', 'idsocio', 'idbingo', 'tipoahorro', 'montoahorro', 'estado')
    list_filter = ('estado', 'tipoahorro')

# ==========================================
# IMAGEN 5: Jugadores y Cartones
# ==========================================
@admin.register(Jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ('aliasjugador', 'correojugador', 'saldocreditojugador', 'estadocuentajugador')
    list_filter = ('estadocuentajugador',)
    search_fields = ('aliasjugador', 'correojugador')

@admin.register(Carton)
class CartonAdmin(admin.ModelAdmin):
    list_display = ('codigocarton', 'idjugador', 'idpartida', 'preciopagado', 'estadocarton')
    list_filter = ('estadocarton',)
    search_fields = ('codigocarton',)

# ==========================================
# IMAGEN 6: Plataforma y Sesiones
# ==========================================
@admin.register(PlataformaJuego)
class PlataformaJuegoAdmin(admin.ModelAdmin):
    list_display = ('nombreplataforma', 'estadoplataforma', 'fechavencimientolicencia')
    list_filter = ('estadoplataforma',)

@admin.register(SesionJuego)
class SesionJuegoAdmin(admin.ModelAdmin):
    list_display = ('idsesion', 'idjugador', 'idplataforma', 'fechainiciosesion', 'estadosesion')
    list_filter = ('estadosesion', 'idplataforma')

# ==========================================
# IMAGEN 7: Regalos y Aportes
# ==========================================
@admin.register(Regalo)
class RegaloAdmin(admin.ModelAdmin):
    list_display = ('nombreregalo', 'valorregalo', 'fechaentregaregalo', 'estadoregalo')
    list_filter = ('estadoregalo',)
    search_fields = ('nombreregalo',)

@admin.register(AporteSemanal)
class AporteSemanalAdmin(admin.ModelAdmin):
    list_display = ('idaporte', 'idsocio', 'numerosemana', 'metodoingreso', 'estadoaporte')
    list_filter = ('estadoaporte', 'metodoingreso')

@admin.register(PartidaBingo)
class PartidaBingoAdmin(admin.ModelAdmin):
    list_display = ('idpartidabingo', 'idbingo', 'nombreronda', 'estadopartida', 'horainicio')
    list_filter = ('estadopartida',)
