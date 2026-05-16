from django.contrib import admin
from django.urls import path
from bingo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.holamundo, name='inicio'),
    path('login/', views.login_jugador, name='login'),
    path('registro/', views.registro_jugador, name='registro'),
    path('logout/', views.cerrar_sesion, name='logout'),
    # Actualizado a bingo_id para reflejar nuestra lógica del HTML
    path('comprar-carton/<int:bingo_id>/', views.comprar_carton, name='comprar_carton'),
    # Nueva ruta para ver los cartones comprados
    path('mis-cartones/', views.mis_cartones, name='mis_cartones'),
]