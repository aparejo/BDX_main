from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from .models import Participante, Categoria, Sucursal, Evento, Puntaje, Subcategoria #Representante
from .forms import ParticipanteForm
from django.http import JsonResponse
from .forms import  CargarPuntosForm #PuntajeForm,
from datetime import datetime, time
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Max
from django.views import View
from django.db.models import Count
from django.contrib.auth.decorators import login_required

class EliminarDuplicadosView(View):
    def get(self, request):
        cedulas_duplicadas = Participante.objects.values('cedula').annotate(count=Count('cedula')).filter(count__gt=1).values_list('cedula', flat=True)

        for cedula in cedulas_duplicadas:
            duplicados = Participante.objects.filter(cedula=cedula).order_by('id')
            duplicados.exclude(id=duplicados.first().id).delete()

        return HttpResponse("Duplicados eliminados correctamente")

def ver_eventos(request):
    eventos = Evento.objects.all()
    return render(request, 'eventos.html', {'eventos': eventos})

@login_required
def BASE(request):
    return render(request, 'base.html')


class ParticipantesListView(ListView):
    model = Participante
    template_name = 'participantes.html'
    context_object_name = 'participantes'
    paginate_by = 50

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        participantes = context['participantes']
        puntajes = Puntaje.objects.filter(participante__in=participantes).select_related('evento', 'categoria', 'subcategoria')
        puntajes = puntajes.values('participante_id','participante__nombre', 'participante__apellido', 'participante__cedula', 'categoria__nombre', 'subcategoria__nombre', 'marca', 'fecha')
        puntajes = puntajes.annotate(max_fecha=Max('fecha')).order_by('-max_fecha')

        context['puntajes'] = puntajes
        return context
    
class ParticipanteDetailView(DetailView):
    model = Participante
    template_name = 'participante.html'
    context_object_name = 'participante'
    categorias = Categoria.objects.all()
""""
class PantallaView(View):
    def get(self, request, id_sucursal):
        sucursal = Sucursal.objects.get(pk=id_sucursal)
        evento = Evento.objects.filter(sucursal=sucursal).latest('fecha_inicio')
        min_marca = 0  # Asigna el valor mínimo deseado para el puntaje
        max_marca = 100
        puntajes = Puntaje.objects.filter(evento=evento, marca__gte=min_marca, marca__lte=max_marca)

        return render(request, 'pantalla.html', {'evento': evento, 'puntajes': puntajes})
"""
class PantallaView(View):
    def get(self, request, id_sucursal):
        sucursal = Sucursal.objects.get(pk=id_sucursal)
        evento = Evento.objects.filter(sucursal=sucursal).latest('fecha_inicio')

        # Obtener los últimos 5 puntajes para cada categoría
        categorias = Categoria.objects.filter(evento=evento)
        ultimos_participantes = {}

        for categoria in categorias:
            puntajes_categoria = Puntaje.objects.filter(evento=evento, categoria=categoria).order_by('-fecha')[:5]

            if categoria.nombre == "Básquetbol Femenino":
                if puntajes_categoria:
                    ultimos_participantes['nombrebf1'] = puntajes_categoria[0].participante.nombre
                    ultimos_participantes['apellidobf1'] = puntajes_categoria[0].participante.apellido
                    ultimos_participantes['subcategoriabf1'] = puntajes_categoria[0].subcategoria.nombre
                    ultimos_participantes['puntajebf1'] = puntajes_categoria[0].marca
                else:
                    ultimos_participantes['nombrebf1'] = ''
                    ultimos_participantes['apellidobf1'] = ''
                    ultimos_participantes['subcategoriabf1'] = ''
                    ultimos_participantes['puntajebf1'] = ''

                if len(puntajes_categoria) > 1:

                    ultimos_participantes['nombrebf2'] = puntajes_categoria[1].participante.nombre
                    ultimos_participantes['apellidobf2'] = puntajes_categoria[1].participante.apellido
                    ultimos_participantes['subcategoriabf2'] = puntajes_categoria[1].subcategoria.nombre
                    ultimos_participantes['puntajebf2'] = puntajes_categoria[1].marca
                else:
                    ultimos_participantes['nombrebf2'] = ''
                    ultimos_participantes['apellidobf2'] = ''
                    ultimos_participantes['subcategoriabf2'] = ''
                    ultimos_participantes['puntajebf2'] = ''

                if len(puntajes_categoria) > 2:

                    ultimos_participantes['nombrebf3'] = puntajes_categoria[2].participante.nombre
                    ultimos_participantes['apellidobf3'] = puntajes_categoria[2].participante.apellido
                    ultimos_participantes['subcategoriabf3'] = puntajes_categoria[2].subcategoria.nombre
                    ultimos_participantes['puntajebf3'] = puntajes_categoria[2].marca
                
                else:
                    ultimos_participantes['nombrebf3'] = ''
                    ultimos_participantes['apellidobf3'] = ''
                    ultimos_participantes['subcategoriabf3'] = ''
                    ultimos_participantes['puntajebf3'] = ''

                if len(puntajes_categoria) > 3:

                    ultimos_participantes['nombrebf4'] = puntajes_categoria[3].participante.nombre
                    ultimos_participantes['apellidobf4'] = puntajes_categoria[3].participante.apellido
                    ultimos_participantes['subcategoriabf4'] = puntajes_categoria[3].subcategoria.nombre
                    ultimos_participantes['puntajebf4'] = puntajes_categoria[3].marca
                
                else:
                    ultimos_participantes['nombrebf4'] = ''
                    ultimos_participantes['apellidobf4'] = ''
                    ultimos_participantes['subcategoriabf4'] = ''
                    ultimos_participantes['puntajebf4'] = ''

                if len(puntajes_categoria) > 4:
                    ultimos_participantes['nombrebf5'] = puntajes_categoria[4].participante.nombre
                    ultimos_participantes['apellidobf5'] = puntajes_categoria[4].participante.apellido
                    ultimos_participantes['subcategoriabf5'] = puntajes_categoria[4].subcategoria.nombre
                    ultimos_participantes['puntajebf5'] = puntajes_categoria[4].marca
                
                else:
                    ultimos_participantes['nombrebf5'] = ''
                    ultimos_participantes['apellidobf5'] = ''
                    ultimos_participantes['subcategoriabf5'] = ''
                    ultimos_participantes['puntajebf5'] = ''

            elif categoria.nombre == "Básquetbol Masculino":
                if puntajes_categoria:
                    ultimos_participantes['nombrebm1'] = puntajes_categoria[0].participante.nombre
                    ultimos_participantes['apellidobm1'] = puntajes_categoria[0].participante.apellido
                    ultimos_participantes['subcategoriabm1'] = puntajes_categoria[0].subcategoria.nombre
                    ultimos_participantes['puntajebm1'] = puntajes_categoria[0].marca
                
                else:
                    ultimos_participantes['nombrebm1'] = ''
                    ultimos_participantes['apellidobm1'] = ''
                    ultimos_participantes['subcategoriabm1'] = ''
                    ultimos_participantes['puntajebm1'] = ''

                if len(puntajes_categoria) > 1:
    
                    ultimos_participantes['nombrebm2'] = puntajes_categoria[1].participante.nombre
                    ultimos_participantes['apellidobm2'] = puntajes_categoria[1].participante.apellido
                    ultimos_participantes['subcategoriabm2'] = puntajes_categoria[1].subcategoria.nombre
                    ultimos_participantes['puntajebm2'] = puntajes_categoria[1].marca
                
                else:
                    ultimos_participantes['nombrebm2'] = ''
                    ultimos_participantes['apellidobm2'] = ''
                    ultimos_participantes['subcategoriabm2'] = ''
                    ultimos_participantes['puntajebm2'] = ''

                if len(puntajes_categoria) > 2:
    
                    ultimos_participantes['nombrebm3'] = puntajes_categoria[2].participante.nombre
                    ultimos_participantes['apellidobm3'] = puntajes_categoria[2].participante.apellido
                    ultimos_participantes['subcategoriabm3'] = puntajes_categoria[2].subcategoria.nombre
                    ultimos_participantes['puntajebm3'] = puntajes_categoria[2].marca
                
                else:
                    ultimos_participantes['nombrebm3'] = ''
                    ultimos_participantes['apellidobm3'] = ''
                    ultimos_participantes['subcategoriabm3'] = ''
                    ultimos_participantes['puntajebm3'] = ''

                if len(puntajes_categoria) > 3:
    
                    ultimos_participantes['nombrebm4'] = puntajes_categoria[3].participante.nombre
                    ultimos_participantes['apellidobm4'] = puntajes_categoria[3].participante.apellido
                    ultimos_participantes['subcategoriabm4'] = puntajes_categoria[3].subcategoria.nombre
                    ultimos_participantes['puntajebm4'] = puntajes_categoria[3].marca
                
                else:
                    ultimos_participantes['nombrebm4'] = ''
                    ultimos_participantes['apellidobm4'] = ''
                    ultimos_participantes['subcategoriabm4'] = ''
                    ultimos_participantes['puntajebm4'] = ''

                if len(puntajes_categoria) > 4:
                
                    ultimos_participantes['nombrebm5'] = puntajes_categoria[4].participante.nombre
                    ultimos_participantes['apellidobm5'] = puntajes_categoria[4].participante.apellido
                    ultimos_participantes['subcategoriabm5'] = puntajes_categoria[4].subcategoria.nombre
                    ultimos_participantes['puntajebm5'] = puntajes_categoria[4].marca
                
                else:
                    ultimos_participantes['nombrebm5'] = ''
                    ultimos_participantes['apellidobm5'] = ''
                    ultimos_participantes['subcategoriabm5'] = ''
                    ultimos_participantes['puntajebm5'] = ''
                    

            elif categoria.nombre == "Fútbol Femenino":
                
                if puntajes_categoria:
                    
                    ultimos_participantes['nombreff1'] = puntajes_categoria[0].participante.nombre
                    ultimos_participantes['apellidoff1'] = puntajes_categoria[0].participante.apellido
                    ultimos_participantes['subcategoriaff1'] = puntajes_categoria[0].subcategoria.nombre
                    ultimos_participantes['puntajeff1'] = puntajes_categoria[0].marca
                
                else:
                    ultimos_participantes['nombreff1'] = ''
                    ultimos_participantes['apellidoff1'] = ''
                    ultimos_participantes['subcategoriaff1'] = ''
                    ultimos_participantes['puntajeff1'] = ''

                if len(puntajes_categoria) > 1:
                    
                    ultimos_participantes['nombreff2'] = puntajes_categoria[1].participante.nombre
                    ultimos_participantes['apellidoff2'] = puntajes_categoria[1].participante.apellido
                    ultimos_participantes['subcategoriaff2'] = puntajes_categoria[1].subcategoria.nombre
                    ultimos_participantes['puntajeff2'] = puntajes_categoria[1].marca
                
                else:
                    ultimos_participantes['nombreff2'] = ''
                    ultimos_participantes['apellidoff2'] = ''
                    ultimos_participantes['subcategoriaff2'] = ''
                    ultimos_participantes['puntajeff2'] = ''

                if len(puntajes_categoria) > 2:
                    
                    ultimos_participantes['nombreff3'] = puntajes_categoria[2].participante.nombre
                    ultimos_participantes['apellidoff3'] = puntajes_categoria[2].participante.apellido
                    ultimos_participantes['subcategoriaff3'] = puntajes_categoria[2].subcategoria.nombre
                    ultimos_participantes['puntajeff3'] = puntajes_categoria[2].marca
                
                else:
                    ultimos_participantes['nombreff3'] = ''
                    ultimos_participantes['apellidoff3'] = ''
                    ultimos_participantes['subcategoriaff3'] = ''
                    ultimos_participantes['puntajeff3'] = ''
                
                if len(puntajes_categoria) > 3:
                    
                    ultimos_participantes['nombreff4'] = puntajes_categoria[3].participante.nombre
                    ultimos_participantes['apellidoff4'] = puntajes_categoria[3].participante.apellido
                    ultimos_participantes['subcategoriaff4'] = puntajes_categoria[3].subcategoria.nombre
                    ultimos_participantes['puntajeff4'] = puntajes_categoria[3].marca
                
                else:
                    ultimos_participantes['nombreff4'] = ''
                    ultimos_participantes['apellidoff4'] = ''
                    ultimos_participantes['subcategoriaff4'] = ''
                    ultimos_participantes['puntajeff4'] = ''
                
                if len(puntajes_categoria) > 4:
                    
                    ultimos_participantes['nombreff5'] = puntajes_categoria[4].participante.nombre
                    ultimos_participantes['apellidoff5'] = puntajes_categoria[4].participante.apellido
                    ultimos_participantes['subcategoriaff5'] = puntajes_categoria[4].subcategoria.nombre
                    ultimos_participantes['puntajeff5'] = puntajes_categoria[4].marca
                
                else:
                    ultimos_participantes['nombreff5'] = ''
                    ultimos_participantes['apellidoff5'] = ''
                    ultimos_participantes['subcategoriaff5'] = ''
                    ultimos_participantes['puntajeff5'] = ''

            elif categoria.nombre == "Fútbol Masculino":
                
                if puntajes_categoria:
                    
                    ultimos_participantes['nombrefm1'] = puntajes_categoria[0].participante.nombre
                    ultimos_participantes['apellidofm1'] = puntajes_categoria[0].participante.apellido
                    ultimos_participantes['subcategoriafm1'] = puntajes_categoria[0].subcategoria.nombre
                    ultimos_participantes['puntajefm1'] = puntajes_categoria[0].marca
                else:
                    ultimos_participantes['nombrefm1'] = ''
                    ultimos_participantes['apellidofm1'] = ''
                    ultimos_participantes['subcategoriafm1'] = ''
                    ultimos_participantes['puntajefm1'] = ''

                if len(puntajes_categoria) > 1:
                
                    ultimos_participantes['nombrefm2'] = puntajes_categoria[1].participante.nombre
                    ultimos_participantes['apellidofm2'] = puntajes_categoria[1].participante.apellido
                    ultimos_participantes['subcategoriafm2'] = puntajes_categoria[1].subcategoria.nombre
                    ultimos_participantes['puntajefm2'] = puntajes_categoria[1].marca
                
                else:
                    ultimos_participantes['nombrefm2'] = ''
                    ultimos_participantes['apellidofm2'] = ''
                    ultimos_participantes['subcategoriafm12'] = ''
                    ultimos_participantes['puntajefm2'] = ''
                    
                if len(puntajes_categoria) > 2:

                    ultimos_participantes['nombrefm3'] = puntajes_categoria[2].participante.nombre
                    ultimos_participantes['apellidofm3'] = puntajes_categoria[2].participante.apellido
                    ultimos_participantes['subcategoriafm3'] = puntajes_categoria[2].subcategoria.nombre
                    ultimos_participantes['puntajefm3'] = puntajes_categoria[2].marca
                
                else:
                    ultimos_participantes['nombrefm3'] = ''
                    ultimos_participantes['apellidofm3'] = ''
                    ultimos_participantes['subcategoriafm3'] = ''
                    ultimos_participantes['puntajefm3'] = ''
                    
                if len(puntajes_categoria) > 3:

                    ultimos_participantes['nombrefm4'] = puntajes_categoria[3].participante.nombre
                    ultimos_participantes['apellidofm4'] = puntajes_categoria[3].participante.apellido
                    ultimos_participantes['subcategoriafm4'] =puntajes_categoria[3].subcategoria.nombre
                    ultimos_participantes['puntajefm4'] = puntajes_categoria[3].marca
                
                else:
                    ultimos_participantes['nombrefm4'] = ''
                    ultimos_participantes['apellidofm4'] = ''
                    ultimos_participantes['subcategoriafm4'] = ''
                    ultimos_participantes['puntajefm4'] = ''
                    
                if len(puntajes_categoria) > 4:
                
                    ultimos_participantes['nombrefm5'] = puntajes_categoria[4].participante.nombre
                    ultimos_participantes['apellidofm5'] = puntajes_categoria[4].participante.apellido
                    ultimos_participantes['subcategoriafm5'] = puntajes_categoria[4].subcategoria.nombre
                    ultimos_participantes['puntajefm5'] = puntajes_categoria[4].marca
                
                else:
                    ultimos_participantes['nombrefm5'] = ''
                    ultimos_participantes['apellidofm5'] = ''
                    ultimos_participantes['subcategoriafm5'] = ''
                    ultimos_participantes['puntajefm5'] = ''

        context = {
            'evento': evento,
            'ultimos_participantes': ultimos_participantes
        }

        return render(request, 'pantalla.html', context)

@login_required  
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

@login_required
def crear_participante(request, cedula=None):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            participante = form.save(commit=False)
            participante.save()
            return redirect('../participantes.html')
    else:
        form = ParticipanteForm(initial={'cedula': cedula}) if cedula else ParticipanteForm()
  
    return render(request, 'crear_participante.html', {'form': form, 'cedula': cedula})


def guardar_participante(request):
    if request.method == 'POST':
        form = ParticipanteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../participantes.html')
    else:
        form = ParticipanteForm()
    
    return render(request, 'formulario_participante.html', {'form': form})

@login_required
def participante(request, participante_id):
    participante = Participante.objects.get(id=participante_id)
    puntajes = Puntaje.objects.filter(participante=participante).order_by('-fecha').select_related('evento', 'categoria', 'subcategoria')

    context = {
        'participante': participante,
        'puntajes': puntajes
    }

    return render(request, 'participante.html', context)

@login_required
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

@login_required
def cargar_puntos(request, participante_id):
    participante = Participante.objects.get(id=participante_id)
    
    if request.method == 'POST':
        form = CargarPuntosForm(request.POST)
        form.fields['categoria'].queryset = Categoria.objects.all()
        form.fields['subcategoria'].queryset = Subcategoria.objects.all()
        
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            marca = form.cleaned_data['marca']
            evento = form.cleaned_data['evento']
            categoria = form.cleaned_data['categoria']
            subcategoria = form.cleaned_data['subcategoria']
            
            fecha_tiempo = datetime.combine(fecha, time.min)
            
            puntaje = Puntaje(
                fecha=fecha_tiempo,
                marca=marca,
                participante=participante,
                evento=evento,
                categoria=categoria,
                subcategoria=subcategoria
            )
            puntaje.save()
            
            return HttpResponseRedirect('../../participante/' + str(participante_id))
    else:
        form = CargarPuntosForm()
        form.fields['categoria'].queryset = Categoria.objects.all()
        form.fields['subcategoria'].queryset = Subcategoria.objects.all()
    
    return render(request, 'participante.html', {'form': form, 'participante': participante})

def obtener_categorias(request, evento_id):
    categorias = Categoria.objects.filter(evento_id=evento_id).values('id', 'nombre')
    return JsonResponse(list(categorias), safe=False)

def buscar_participante(request):
    if request.method == 'POST':
        cedula = request.POST['cedula']
        try:
            participante = Participante.objects.get(cedula=cedula)
            return HttpResponseRedirect(f'/participante/{participante.id}/')
        except Participante.DoesNotExist:
            return HttpResponseRedirect(f'/crear_participante/{cedula}/')
    else:
        return render(request, 'buscar_participante.html')
    
    
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