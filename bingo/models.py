from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class TipoSocio(models.Model):
  nombre = models.CharField(max_length=50) # Ej: "Administrador", "Jugador Regular"
 
  def __str__(self):
    return self.nombre
 
class Socio(models.Model):
  nombres = models.CharField(max_length=100)
  tipo_socio = models.ForeignKey('TipoSocio', on_delete=models.CASCADE)

  def __str__(self):
    return self.nombres

class Prestamo(models.Model):
  nombreprestamo = models.CharField(max_length=100)
  monto = models.DecimalField(max_digits=10, decimal_places=2)
  socio = models.ForeignKey(Socio, on_delete=models.CASCADE)

  def __str__(self):
    return self.nombreprestamo

class TipoJugador(models.Model):
  nombre = models.CharField(max_length=50) # Ej: "Virtual" o "Presencial"

  def __str__(self):
    return self.nombre
 
class Jugador(models.Model):
  usuario = models.OneToOneField(User, on_delete=models.CASCADE)
  tipo = models.ForeignKey(TipoJugador, on_delete=models.CASCADE)
  creditos = models.IntegerField(default=0)
 
  def __str__(self):
    return f"{self.usuario.username} - {self.tipo.nombre}"
