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
from reto.views import pantalla_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from reto import views
from reto.views import ParticipantesListView
from reto.views import ParticipanteDetailView
from reto import views
from reto.views import crear_evento, lista_eventos
from reto.views import BASE1, guardar_participante, guardar_representante





class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('1/', pantalla_view, name='pantalla'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.BASE, name='BASE'),
    path('guardar_participante/', guardar_participante, name='guardar-participante'),
    path('guardar-representante/', guardar_representante, name='guardar-representante'),
    path('crear_participante/', BASE1, name='crear_participante'),
    path('participantes.html', ParticipantesListView.as_view(), name='participantes_list'),
    path('participante/<int:pk>/', ParticipanteDetailView.as_view(), name='participante_detail'),
    path('crear_evento/', crear_evento, name='crear_evento'),
    path('lista_eventos/', lista_eventos, name='lista_eventos'),
    # otras rutas de tu aplicación
]
