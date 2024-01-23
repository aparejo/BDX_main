from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.views.generic import DetailView
from reto.models import Participante, Categoria, Sucursal, Evento
from datetime import datetime
from django.utils import timezone
from django.contrib import messages
from django.views.generic.edit import CreateView
from django import forms
from .models import Participante



def ver_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})
def BASE(request):
    return render(request, 'base.html')
def BASE1(request):
    sucursal = Sucursal.objects.first()  # Ejemplo, obtén la sucursal adecuada
    categorias = Categoria.objects.all() 
    evento = Evento.objects.first() 

    context = {
        'sucursal': sucursal,
        'categorias': categorias,
        'evento': evento,
    }
    return render(request, 'crear_participante.html', context)
class ParticipantesListView(ListView):
    model = Participante
    template_name = 'participantes.html'
    context_object_name = 'reto'
    paginate_by = 20
    
class ParticipanteDetailView(DetailView):
    model = Participante
    template_name = 'participante.html'
    context_object_name = 'participante'
    categorias = Categoria.objects.all()
    
def pantalla_view(request):
    sucursal = Sucursal.objects.first()  # Ejemplo, obtén la sucursal adecuada
    categorias = Categoria.objects.all() 
    participantes = Participante.objects.filter(sucursal=sucursal).select_related('subcategoria')
    evento = Evento.objects.first() 

    context = {
        'sucursal': sucursal,
        'categorias': categorias,
        'participantes': participantes,
        'evento': evento,
    }

    return render(request, 'pantalla.html', context)

def crear_evento(request):
    sucursales = Sucursal.objects.all()  # Obtener todas las sucursales
    if request.method == 'POST':
        # Procesar los datos enviados por el formulario
        nombre = request.POST['nombre']
        fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%dT%H:%M')
        fecha_fin = datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%dT%H:%M')
        sucursal_id = int(request.POST['sucursal'])
        record = request.POST['record']
        participacion = request.POST['participacion']
        status = request.POST['status']
        tiene_categoria = 'tiene_categoria' in request.POST
        tiene_subcategoria = 'tiene_subcategoria' in request.POST
        
        # Crear una instancia del evento
        evento = Evento(nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, 
                        sucursal_id=sucursal_id, record=record, participacion=participacion,
                        status=status, tiene_categoria=tiene_categoria, tiene_subcategoria=tiene_subcategoria)
        evento.save()
        
        # Redirigir a la página que muestra la lista de eventos
        return redirect('lista_eventos')
    else:
        # Mostrar el formulario para crear un evento
        return render(request, 'crear_evento2.html', {'sucursales': sucursales})
    
def lista_eventos(request):
    eventos = Evento.objects.order_by('-fecha_inicio')  # Obtener eventos ordenados por fecha de inicio descendente
    return render(request, 'lista_eventos2.html', {'eventos': eventos})

def guardar_participante(request):
    # Obtener los datos del formulario
    # ...

    # Verificar si el participante ya ha participado en un evento dentro de los límites establecidos
    if participante.evento.opciones_participacion == "unica":
        participaciones = Participante.objects.filter(usuario=request.user, evento=participante.evento)
        if participaciones.exists():
            messages.error(request, "Ya has participado en este evento.")

    elif participante.evento.opciones_participacion == "unica_dia":
        fecha_actual = timezone.now().date()
        participaciones = Participante.objects.filter(usuario=request.user, evento=participante.evento, fecha=fecha_actual)
        if participaciones.exists():
            messages.error(request, "Ya has participado en este evento hoy. Podrás participar nuevamente mañana.")

    elif participante.evento.opciones_participacion == "unica_semana":
        fecha_actual = timezone.now().date()
        fecha_inicio_semana = fecha_actual - datetime.timedelta(days=fecha_actual.weekday())
        fecha_fin_semana = fecha_inicio_semana + datetime.timedelta(days=6)
        participaciones = Participante.objects.filter(usuario=request.user, evento=participante.evento, fecha__range=[fecha_inicio_semana, fecha_fin_semana])
        if participaciones.exists():
            messages.error(request, "Ya has participado en este evento por esta semana. Podrás participar nuevamente la proxima semana.")

    elif participante.evento.opciones_participacion == "unica_mes":
        fecha_actual = timezone.now().date()
        fecha_inicio_mes = fecha_actual.replace(day=1)
        fecha_fin_mes = fecha_inicio_mes.replace(day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1])
        participaciones = Participante.objects.filter(usuario=request.user, evento=participante.evento, fecha__range=[fecha_inicio_mes, fecha_fin_mes])
        if participaciones.exists():
            messages.error(request, "Ya has participado en este evento en este mes. Podrás participar nuevamente la proxima semana.")

    # Guardar el participante y la fecha de la última participación
    participante.save()
    participante.ultima_participacion = timezone.now()
    participante.save()
class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = '__all__'    
def participante(request):
    # Obtener el participante actual
    participante = Participante.objects.get(usuario=request.user)

    # Obtener los puntajes del participante ordenados por fecha descendente
    puntajes = Puntaje.objects.filter(participante=participante).order_by('-fecha')

    # Pasar los datos a la plantilla
    context = {
        'participante': participante,
        'puntajes': puntajes
    }

    return render(request, 'participante.html', context)

def registrar_puntaje(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.POST.get('fecha')
        puntos = request.POST.get('puntos')

        # Crear el objeto de puntaje y guardarlo
        puntaje = Puntaje(participante=participante, fecha=fecha, puntos=puntos)
        puntaje.save()
        
def guardar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save()
            # Realiza cualquier acción adicional que necesites, como enviar una respuesta o redirigir a otra página
            return redirect('participantes')  # Reemplaza 'nombre_de_la_vista' con el nombre de la vista a la que deseas redirigir
    else:
        form = ParticipanteForm()
    
    return render(request, 'guardar_participante.html', {'form': form})

class GuardarParticipanteView(CreateView):
    model = Participante
    form_class = ParticipanteForm
    template_name = 'guardar_participante.html'
    success_url = '/ruta_de_exito/'  # Reemplaza '/ruta_de_exito/' con la URL a la que deseas redirigir después de guardar el participante