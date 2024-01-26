"""
URL configuration for BDX project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from reto import views
from reto.views import ParticipantesListView
from reto.views import ParticipanteDetailView
from reto import views
from reto.views import PantallaView
from reto.views import crear_evento, lista_eventos
from reto.views import guardar_participante, guardar_puntaje, obtener_categorias #guardar_representante





class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:id_sucursal>/', PantallaView.as_view(), name='pantalla'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.BASE, name='BASE'),
    path('buscar-participante/', views.buscar_participante, name='buscar_participante'),
    path('participante/<int:participante_id>/', views.participante, name='participante'),
    path('guardar-participante/', views.guardar_participante, name='guardar-participante'),
    #path('guardar-representante/', guardar_representante, name='guardar-representante'),
    path('crear_participante/<str:cedula>/', views.crear_participante, name='crear_participante'),
    path('participantes.html', ParticipantesListView.as_view(), name='participantes_list'),
    path('participante/<int:pk>/', ParticipanteDetailView.as_view(), name='participante_detail'),
    path('crear_evento/', crear_evento, name='crear_evento'),
    path('lista_eventos/', lista_eventos, name='lista_eventos'),
    path('guardar-puntaje/', guardar_puntaje, name='guardar_puntaje'),
    path('participante/<int:pk>/guardar-puntaje/', guardar_puntaje, name='guardar_puntaje'),
    path('cargar-puntos/<int:participante_id>/', views.cargar_puntos, name='cargar_puntos'),
    path('obtener_categorias/<int:evento_id>/', views.obtener_categorias, name='obtener_categorias'),
    #path('formulario_representante/', views.formulario_representante, name='formulario_representante'),
    # otras rutas de tu aplicación
]
