from django.db import models
from django.db.models import Q
from django.utils import timezone

# ==========================================
# IMAGEN 1: Socios
# ==========================================
class TipoSocio(models.Model):
    idtiposocio = models.AutoField(primary_key=True)
    nombretiposocio = models.CharField(max_length=100, unique=True)
    roltiposocio = models.CharField(max_length=50, unique=True)
    descripciondetiposocio = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'TipoSocio'

class Socio(models.Model):
    idsocio = models.AutoField(primary_key=True)
    idtiposocio = models.ForeignKey(TipoSocio, on_delete=models.RESTRICT, db_column='idtiposocio')
    primernombresocio = models.CharField(max_length=40)
    segundonombresocio = models.CharField(max_length=40, null=True, blank=True)
    primerapellidosocio = models.CharField(max_length=40)
    segundoapellidosocio = models.CharField(max_length=40)
    cisocio = models.CharField(max_length=10, unique=True)
    fechanacimientosocio = models.DateField()
    telefonopersonalsocio = models.CharField(max_length=10)
    telefonotrabajosocio = models.CharField(max_length=25, null=True, blank=True)
    direcciondomiciliosocio = models.CharField(max_length=255)
    direcciontrabajosocio = models.CharField(max_length=255, null=True, blank=True)
    sexosocio = models.CharField(max_length=1, null=True, blank=True)
    estadosocio = models.CharField(max_length=10)

    class Meta:
        db_table = 'Socio'
        constraints = [
            models.CheckConstraint(
                condition=Q(sexosocio__in=['H', 'M']),
                name='chk_socio_sexosocio'
            ),
            models.CheckConstraint(
                condition=Q(estadosocio__in=['Activo', 'Inactivo']),
                name='chk_socio_estadosocio'
            )
        ]


# ==========================================
# IMAGEN 2: Cuentas
# ==========================================
class CuentaBancaria(models.Model):
    idcuentabancaria = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(Socio, on_delete=models.RESTRICT, db_column='idsocio')
    nombrebanco = models.CharField(max_length=100)
    numerocuenta = models.CharField(max_length=30, unique=True)
    tipocuenta = models.CharField(max_length=20)
    esprincipal = models.BooleanField(default=False, unique=True) 
    fecharegistro = models.DateTimeField(default=timezone.now)
    estadocuenta = models.CharField(max_length=10)

    class Meta:
        db_table = 'CuentaBancaria'
        constraints = [
            models.CheckConstraint(
                condition=Q(tipocuenta__in=['Ahorro', 'Corriente']),
                name='chk_cuentabancaria_tipocuenta'
            )
        ]

class MetodoPago(models.Model):
    idmetodopago = models.AutoField(primary_key=True)
    nombremetodopago = models.CharField(max_length=50, unique=True)
    descripcionmetodopago = models.CharField(max_length=200, null=True, blank=True)
    estadometodopago = models.BooleanField(default=True)
    urlmetodopago = models.CharField(max_length=255)

    class Meta:
        db_table = 'MetodoPago'


# ==========================================
# IMAGEN 3: Préstamos y Pagos
# ==========================================
class Prestamo(models.Model):
    idprestamo = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(Socio, on_delete=models.RESTRICT, db_column='idsocio')
    montoprestamosolicitado = models.DecimalField(max_digits=12, decimal_places=2)
    tasainteres = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    montototalpagar = models.DecimalField(max_digits=12, decimal_places=2)
    saldopendiente = models.DecimalField(max_digits=12, decimal_places=2)
    numerocuotas = models.IntegerField(default=1)
    fechasolicitud = models.DateField()
    fechavencimiento = models.DateField()
    estadoprestamo = models.CharField(max_length=20)

    class Meta:
        db_table = 'Prestamo'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadoprestamo__in=['Solicitado', 'Aprobado', 'En espera', 'Liquidado']),
                name='chk_prestamo_estadoprestamo'
            ),
            models.CheckConstraint(
                condition=Q(montoprestamosolicitado__gte=0),
                name='chk_prestamo_montoprestamosolicitado'
            ),
            models.CheckConstraint(
                condition=Q(numerocuotas__gte=1),
                name='chk_prestamo_numerocuotas'
            )
        ]

class Pago(models.Model):
    idpago = models.AutoField(primary_key=True)
    idprestamo = models.ForeignKey(Prestamo, on_delete=models.RESTRICT, db_column='idprestamo')
    idmetodopago = models.ForeignKey(MetodoPago, on_delete=models.RESTRICT, db_column='idmetodopago')
    montopagado = models.DecimalField(max_digits=10, decimal_places=2)
    numeroreferencia = models.CharField(max_length=50, unique=True, null=True, blank=True)
    fechapago = models.DateTimeField()
    fechaconfirmacionadmin = models.DateTimeField(null=True, blank=True)
    comprobantepago = models.CharField(max_length=255, null=True, blank=True)
    estadopago = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'Pago'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadopago__in=['Pendiente', 'Validado', 'Rechazado']),
                name='chk_pago_estadopago'
            )
        ]


# ==========================================
# IMAGEN 4: Bingo y Ahorros
# ==========================================
class Bingo(models.Model):
    idbingo = models.AutoField(primary_key=True)
    titulobingo = models.CharField(max_length=150)
    fechaprogramadabingo = models.DateTimeField()
    tipobingo = models.CharField(max_length=20)
    lugarbingo = models.CharField(max_length=255, null=True, blank=True)
    urlsesionbingo = models.CharField(max_length=255, null=True, blank=True)
    preciocarton = models.DecimalField(max_digits=10, decimal_places=2)
    premiomayor = models.DecimalField(max_digits=10, decimal_places=2)
    descripcionpremiomayor = models.CharField(max_length=100)
    estadobingo = models.CharField(max_length=20)
    rutaimagenpremiomayor = models.CharField(max_length=300, null=True, blank=True)
    urlvideopromocional = models.CharField(max_length=300, null=True, blank=True)
    descripcionpremios = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        db_table = 'Bingo'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadobingo__in=['Programado', 'En Curso', 'Finalizado', 'Cancelado']),
                name='chk_bingo_estadobingo'
            )
        ]

class Ahorro(models.Model):
    idahorro = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(Socio, on_delete=models.RESTRICT, db_column='idsocio')
    idbingo = models.ForeignKey(Bingo, on_delete=models.RESTRICT, db_column='idbingo')
    tipoahorro = models.CharField(max_length=50)
    montoahorro = models.DecimalField(max_digits=10, decimal_places=2)
    fechaahorro = models.DateTimeField()
    comentarioahorro = models.CharField(max_length=100, null=True, blank=True)
    estado = models.CharField(max_length=25)

    class Meta:
        db_table = 'Ahorro'
        constraints = [
            models.CheckConstraint(
                condition=Q(tipoahorro__in=['Obligatorio', 'Voluntario']),
                name='chk_ahorro_tipoahorro'
            ),
            models.CheckConstraint(
                condition=Q(estado__in=['Activo', 'Inactivo']),
                name='chk_ahorro_estado'
            )
        ]


# ==========================================
# IMAGEN 5: Jugadores
# ==========================================
class Jugador(models.Model):
    idjugador = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(Socio, on_delete=models.SET_NULL, null=True, blank=True, db_column='idsocio')
    avatarjugador = models.CharField(max_length=255, null=True, blank=True)
    aliasjugador = models.CharField(max_length=100, unique=True, null=True, blank=True)
    correojugador = models.CharField(max_length=200, unique=True, null=True, blank=True)
    fecharegistrojugador = models.DateTimeField()
    saldocreditojugador = models.DecimalField(max_digits=10, decimal_places=2)
    estadocuentajugador = models.CharField(max_length=20)

    class Meta:
        db_table = 'Jugador'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadocuentajugador__in=['Activo', 'Suspendido', 'Moroso']),
                name='chk_jugador_estadocuentajugador'
            )
        ]


# ==========================================
# NUEVO: PARTIDA BINGO
# ==========================================
class PartidaBingo(models.Model):
    idpartidabingo = models.AutoField(primary_key=True)
    idbingo = models.ForeignKey(Bingo, on_delete=models.RESTRICT, db_column='idbingo')
    idjugadorganador = models.ForeignKey(Jugador, on_delete=models.SET_NULL, null=True, blank=True, db_column='idjugadorganador')
    nombreronda = models.CharField(max_length=100)
    valorefectivo = models.DecimalField(max_digits=10, decimal_places=2)
    premiomaterial = models.CharField(max_length=150)
    estadopartida = models.CharField(max_length=20)
    bolascantadas = models.TextField() # varchar(max)
    ultimabola = models.IntegerField()
    haydesempate = models.BooleanField(null=True, blank=True) # bit
    idbingadores = models.TextField(null=True, blank=True) # varchar(max)
    bolamayordesempate = models.IntegerField(null=True, blank=True)
    horainicio = models.DateTimeField()
    horafin = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'PartidaBingo'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadopartida__in=['En Juego', 'Verificando', 'Desempate', 'Finalizada']),
                name='chk_partidabingo_estadopartida'
            )
        ]


# ==========================================
# IMAGEN 5 (Cont.): Cartones
# ==========================================
class Carton(models.Model):
    idcarton = models.AutoField(primary_key=True)
    idjugador = models.ForeignKey(Jugador, on_delete=models.RESTRICT, null=True, blank=True, db_column='idjugador')
    idpartida = models.ForeignKey(PartidaBingo, on_delete=models.RESTRICT, null=True, blank=True, db_column='idpartida')
    codigocarton = models.CharField(max_length=30, unique=True)
    matriznumeros = models.TextField() 
    indicevictoria = models.IntegerField(default=0, null=True, blank=True)
    preciopagado = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    fechacompra = models.DateTimeField(null=True, blank=True)
    estadocarton = models.CharField(max_length=20, default='Disponible')

    class Meta:
        db_table = 'Carton'
        constraints = [
            models.CheckConstraint(
                condition=Q(preciopagado__gte=0),
                name='chk_carton_preciopagado'
            )
        ]


# ==========================================
# IMAGEN 6: Plataforma y Sesiones
# ==========================================
class PlataformaJuego(models.Model):
    idplataformajuego = models.AutoField(primary_key=True)
    nombreplataforma = models.CharField(max_length=25, unique=True)
    urlplataforma = models.CharField(max_length=255)
    descripcionplataforma = models.CharField(max_length=200, null=True, blank=True)
    estadoplataforma = models.BooleanField()
    fechaadquisicionlicencia = models.DateField(null=True, blank=True)
    fechavencimientolicencia = models.DateField(null=True, blank=True)
    contactoplataforma = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'PlataformaJuego'

class SesionJuego(models.Model):
    idsesion = models.AutoField(primary_key=True)
    idplataforma = models.ForeignKey(PlataformaJuego, on_delete=models.RESTRICT, db_column='idplataforma')
    idjugador = models.ForeignKey(Jugador, on_delete=models.RESTRICT, db_column='idjugador')
    idpartida = models.ForeignKey(PartidaBingo, on_delete=models.RESTRICT, db_column='idpartida') # <--- Cambiado a PartidaBingo
    fechainiciosesion = models.DateTimeField()
    fechafinsesion = models.DateTimeField(null=True, blank=True)
    ipconexion = models.CharField(max_length=50, null=True, blank=True)
    dispositivoconexion = models.CharField(max_length=50, null=True, blank=True)
    estadosesion = models.CharField(max_length=15)
    latenciaping = models.IntegerField(null=True, blank=True)
    navegadorweb = models.CharField(max_length=150, null=True, blank=True)
    tokenconexion = models.CharField(max_length=255, unique=True)
    motivocierre = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'SesionJuego'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadosesion__in=['Activa', 'Finalizada', 'Caida']),
                name='chk_sesionjuego_estadosesion'
            )
        ]


# ==========================================
# IMAGEN 7: Regalos y Aportes
# ==========================================
class Regalo(models.Model):
    idregalo = models.AutoField(primary_key=True)
    nombreregalo = models.CharField(max_length=100)
    descripcionregalo = models.CharField(max_length=200, null=True, blank=True)
    valorregalo = models.DecimalField(max_digits=10, decimal_places=2)
    fechaentregaregalo = models.DateTimeField()
    estadoregalo = models.CharField(max_length=20)
    fechaultimaactualizacion = models.DateTimeField()
    urlimagen = models.CharField(max_length=255)

    class Meta:
        db_table = 'Regalo'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadoregalo__in=['Acumulado', 'Sorteado', 'Entregado']),
                name='chk_regalo_estadoregalo'
            )
        ]

class AporteSemanal(models.Model):
    idaporte = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(Socio, on_delete=models.RESTRICT, db_column='idsocio')
    idregalo = models.ForeignKey(Regalo, on_delete=models.RESTRICT, db_column='idregalo')
    idpartida = models.ForeignKey(PartidaBingo, on_delete=models.RESTRICT, db_column='idpartida')
    numerosemana = models.IntegerField(null=True, blank=True)
    fechaplanificadada = models.DateTimeField()
    fechaentregareal = models.DateTimeField(null=True, blank=True)
    metodoingreso = models.CharField(max_length=50)
    referenciaingreso = models.CharField(max_length=100, null=True, blank=True)
    estadoaporte = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'AporteSemanal'
        constraints = [
            models.CheckConstraint(
                condition=Q(estadoaporte__in=['Al Dia', 'Atrasado']),
                name='chk_aportesemanal_estadoaporte'
            ),
            models.CheckConstraint(
                condition=Q(metodoingreso__in=['Efectivo', 'Transferencia', 'Fisico']),
                name='chk_aportesemanal_metodoingreso'
            )
        ]