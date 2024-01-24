from django import forms
from .models import Participante, Puntaje, Evento, Categoria, Subcategoria
from django import forms
from django.forms.widgets import SelectDateWidget

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'apellido', 'telefono', 'ciudad', 'cedula', 'fecha', 'tieneci']
        
class PuntajeForm(forms.ModelForm):
    class Meta:
        model = Puntaje
        fields = ('fecha', 'marca', 'tiempo', 'participante', 'evento', 'categoria', 'subcategoria')
        
class CargarPuntosForm(forms.Form):
    fecha = forms.DateField(widget=SelectDateWidget)
    marca = forms.CharField(max_length=100, required=False)
    tiempo = forms.CharField(max_length=100, required=False)
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), empty_label=None)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.none(), empty_label=None)
    subcategoria = forms.ModelChoiceField(queryset=Subcategoria.objects.none(), empty_label=None)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evento'].widget.attrs['onchange'] = 'actualizar_categorias();'
        self.fields['categoria'].widget.attrs['onchange'] = 'actualizar_subcategorias();'