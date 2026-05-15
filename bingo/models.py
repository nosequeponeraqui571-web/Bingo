from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class TipoSocio(models.Model):
    idtiposocio = models.AutoField(primary_key=True)
    nombretiposocio = models.CharField(max_length=100, unique=True, null=False, blank=False)
    roltiposocio = models.CharField(max_length=50, unique=True, null=False, blank=False)
    descripciondetiposocio = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        db_table = 'TipoSocio'


class Socio(models.Model):
    idsocio = models.AutoField(primary_key=True)
    idtiposocio = models.ForeignKey(
        TipoSocio, 
        on_delete=models.RESTRICT, 
        db_column='idtiposocio'
    )
    primernombresocio = models.CharField(max_length=40, null=False, blank=False)
    segundonombresocio = models.CharField(max_length=40, null=True, blank=True)
    primerapellidosocio = models.CharField(max_length=40, null=False, blank=False)
    segundoapellidosocio = models.CharField(max_length=40, null=False, blank=False)
    cisocio = models.CharField(max_length=10, unique=True, null=False, blank=False)
    fechanacimientosocio = models.DateField(null=False, blank=False)
    telefonopersonalsocio = models.CharField(max_length=10, null=False, blank=False)
    telefonotrabajosocio = models.CharField(max_length=25, null=True, blank=True)
    direcciondomiciliosocio = models.CharField(max_length=255, null=False, blank=False)
    direcciontrabajosocio = models.CharField(max_length=255, null=True, blank=True)
    sexosocio = models.CharField(max_length=1, null=True, blank=True)
    estadosocio = models.CharField(max_length=10, null=False, blank=False)

    class Meta:
        db_table = 'Socio'
        constraints = [
            models.CheckConstraint(
                check=models.Q(sexosocio__in=['H', 'M']), 
                name='chk_socio_sexosocio'
            )
        ]


class SesionJuego(models.Model):
    idsesion = models.AutoField(primary_key=True)
    estadosesion = models.CharField(max_length=20, null=False, blank=False)
    tokenconexion = models.CharField(max_length=255, unique=True, null=False, blank=False)

    class Meta:
        db_table = 'SesionJuego'
        constraints = [
            models.CheckConstraint(
                check=models.Q(estadosesion__in=['Activa', 'Finalizada', 'Caida']), 
                name='chk_sesion_estadosesion'
            )
        ]


class Regalo(models.Model):
    idregalo = models.AutoField(primary_key=True)
    nombreregalo = models.CharField(max_length=100, null=False, blank=False)
    descripcionregalo = models.CharField(max_length=200, null=True, blank=True)
    valorregalo = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    fechaentregaregalo = models.DateTimeField(null=False, blank=False)
    estadoregalo = models.CharField(max_length=20, null=False, blank=False)
    fechaultimaactualizacion = models.DateTimeField(null=False, blank=False)
    urlimagen = models.CharField(max_length=255, null=False, blank=False)

    class Meta:
        db_table = 'Regalo'
        constraints = [
            models.CheckConstraint(
                check=models.Q(estadoregalo__in=['Acumulado', 'Sorteado', 'Entregado']), 
                name='chk_regalo_estadoregalo'
            )
        ]


class AporteSemanal(models.Model):
    idaporte = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(
        Socio, 
        on_delete=models.RESTRICT, 
        db_column='idsocio'
    )
    idregalo = models.ForeignKey(
        Regalo, 
        on_delete=models.RESTRICT, 
        db_column='idregalo'
    )
    idpartida = models.IntegerField(null=True, blank=True) 
    numerosemana = models.IntegerField(null=True, blank=True)
    fechaplanificadada = models.DateTimeField(null=False, blank=False)
    fechaentregareal = models.DateTimeField(null=True, blank=True)
    metodoingreso = models.CharField(max_length=50, null=False, blank=False) 
    referenciaingreso = models.CharField(max_length=100, null=True, blank=True) 
    estadoaporte = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'AporteSemanal'


class Ahorro(models.Model):
    idahorro = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(
        Socio, 
        on_delete=models.RESTRICT, 
        db_column='idsocio'
    )
    fecharegistro = models.DateTimeField(null=False, blank=False)
    montoahorrado = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    origenahorro = models.CharField(max_length=50, null=False, blank=False)
    estadoahorro = models.CharField(max_length=20, null=False, blank=False)
    fechaultimaactualizacion = models.DateTimeField(null=False, blank=False)

    class Meta:
        db_table = 'Ahorro'
        constraints = [
            models.CheckConstraint(
                check=models.Q(estadoahorro__in=['Activo', 'Retirado', 'Congelado']), 
                name='chk_ahorro_estadoahorro'
            )
        ]


class Prestamo(models.Model):
    idprestamo = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(
        Socio, 
        on_delete=models.RESTRICT, 
        db_column='idsocio'
    )
    fechasolicitud = models.DateTimeField(null=False, blank=False)
    montosolicitado = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    plazomeses = models.IntegerField(null=False, blank=False)
    tasa_interes = models.DecimalField(max_digits=5, decimal_places=2, null=False, blank=False)
    estado_prestamo = models.CharField(max_length=20, null=False, blank=False)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'Prestamo'
        constraints = [
            models.CheckConstraint(
                check=models.Q(estado_prestamo__in=['Pendiente', 'Aprobado', 'Rechazado', 'Pagado']), 
                name='chk_prestamo_estado_prestamo'
            ),
            models.CheckConstraint(
                check=models.Q(plazomeses__lte=12), 
                name='chk_prestamo_plazomeses'
            )
        ]


class Garante(models.Model):
    idgarante = models.AutoField(primary_key=True)
    idprestamo = models.ForeignKey(
        Prestamo, 
        on_delete=models.RESTRICT, 
        db_column='idprestamo'
    )
    idsocio = models.ForeignKey(
        Socio, 
        on_delete=models.RESTRICT, 
        db_column='idsocio'
    )
    montogarantia = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    estado_garantia = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'Garante'
        constraints = [
            models.CheckConstraint(
                check=models.Q(estado_garantia__in=['Activo', 'Liberado', 'Ejecutado']), 
                name='chk_garante_estado_garantia'
            )
        ]


class Utilidad(models.Model):
    idutilidad = models.AutoField(primary_key=True)
    idsocio = models.ForeignKey(
        Socio, 
        on_delete=models.RESTRICT, 
        db_column='idsocio'
    )
    fechareparticion = models.DateTimeField(null=False, blank=False)
    montoutilidad = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    origen_utilidad = models.CharField(max_length=50, null=False, blank=False)
    estado_utilidad = models.CharField(max_length=20, null=False, blank=False)

    class Meta:
        db_table = 'Utilidad'
        constraints = [
            models.CheckConstraint(
                check=models.Q(origen_utilidad__in=['Bingo', 'Interes Prestamo']), 
                name='chk_utilidad_origen_utilidad'
            ),
            models.CheckConstraint(
                check=models.Q(estado_utilidad__in=['Pendiente', 'Pagado']), 
                name='chk_utilidad_estado_utilidad'
            )
        ]