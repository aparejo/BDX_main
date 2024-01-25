from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .models import Participante, Categoria, Sucursal, Evento, Puntaje, Subcategoria #Representante
from .forms import ParticipanteForm
from django.http import JsonResponse
from .forms import  CargarPuntosForm #PuntajeForm,
from datetime import datetime, time
from django.http import HttpResponseRedirect

def ver_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})

def BASE(request):
    return render(request, 'base.html')

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
    sucursal = Sucursal.objects.first()
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
    sucursales = Sucursal.objects.all()
    if request.method == 'POST':
        nombre = request.POST['nombre']
        fecha_inicio = datetime.strptime(request.POST['fecha_inicio'], '%Y-%m-%dT%H:%M')
        fecha_fin = datetime.strptime(request.POST['fecha_fin'], '%Y-%m-%dT%H:%M')
        sucursal_id = int(request.POST['sucursal'])
        record = request.POST['record']
        participacion = request.POST['participacion']
        status = request.POST['status']
        tiene_categoria = 'tiene_categoria' in request.POST
        tiene_subcategoria = 'tiene_subcategoria' in request.POST
        
        evento = Evento(nombre=nombre, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, 
                        sucursal_id=sucursal_id, record=record, participacion=participacion,
                        status=status, tiene_categoria=tiene_categoria, tiene_subcategoria=tiene_subcategoria)
        evento.save()
        
        return redirect('lista_eventos')
    else:
        return render(request, 'crear_evento2.html', {'sucursales': sucursales})
    
def lista_eventos(request):
    eventos = Evento.objects.order_by('-fecha_inicio')
    return render(request, 'lista_eventos2.html', {'eventos': eventos})

def crear_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.save()
            return redirect('../participantes.html')
    else:
        form = ParticipanteForm()
  
    return render(request, 'crear_participante.html', {'form': form})

def guardar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../participantes.html')
    else:
        form = ParticipanteForm()
    
    return render(request, 'formulario_participante.html', {'form': form})

def participante(request, participante_id):
    participante = Participante.objects.get(id=participante_id)
    puntajes = Puntaje.objects.filter(participante=participante).order_by('-fecha').select_related('evento', 'categoria', 'subcategoria')

    context = {
        'participante': participante,
        'puntajes': puntajes
    }

    return render(request, 'participante.html', context)

def registrar_puntaje(request):
    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        puntos = request.POST.get('puntos')

        puntaje = Puntaje(participante=participante, fecha=fecha, puntos=puntos)
        puntaje.save()

class GuardarParticipanteView(CreateView):
    model = Participante
    form_class = ParticipanteForm
    template_name = 'guardar_participante.html'
    success_url = 'participantes.html'
    
def guardar_puntaje(request):
    if request.method == 'POST':
        form = PuntajeForm(request.POST)
        if form.is_valid():
            puntaje = form.save()
            puntos = calcular_puntos(puntaje)  # Función para calcular los puntos según el puntaje
            return JsonResponse({'puntos': puntos})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        form = PuntajeForm()
    return render(request, 'guardar_puntaje.html', {'form': form})

def cargar_puntos(request, participante_id):
    # Obtener el participante según su ID
    participante = Participante.objects.get(id=participante_id)
    
    if request.method == 'POST':
        form = CargarPuntosForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario y guardar el puntaje
            
            # Acceder a los datos del formulario
            fecha = form.cleaned_data['fecha']
            marca = form.cleaned_data['marca']
            evento = form.cleaned_data['evento']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']
            
            # Combinar la fecha seleccionada con un tiempo predeterminado (00:00:00)
            fecha_tiempo = datetime.combine(fecha, time.min)
            
            # Crear una instancia del modelo Puntaje y guardarla
            puntaje = Puntaje(
                fecha=fecha_tiempo,
                marca=marca,
                participante=participante,
                evento=evento,
                categoria=categoria,
                subcategoria=subcategoria
            )
            puntaje.save()
            
            # Redireccionar o mostrar un mensaje de éxito
            return HttpResponseRedirect('../../participante/' + str(participante_id))  # Reemplaza '/ruta/redireccionamiento/' por la URL a la que deseas redirigir
            
    else:
        form = CargarPuntosForm()
    
    return render(request, 'participante.html', {'form': form, 'participante': participante})

def obtener_categorias(request, evento_id):
    categorias = Categoria.objects.filter(evento_id=evento_id).values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)
"""
def guardar_representante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        ciudad = request.POST.get('ciudad')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        parentezco = request.POST.get('parentezco')

        representante = Representante(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            ciudad=ciudad,
            fecha_nacimiento=fecha_nacimiento,
            telefono=telefono,
            correo=correo,
            parentezco=parentezco
        )

        representante.save()
    return redirect('participantes')
"""