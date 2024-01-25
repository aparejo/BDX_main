from django import forms
from .models import Participante, Puntaje, Evento, Categoria, Subcategoria
from django import forms
from django.forms.widgets import SelectDateWidget

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'apellido', 'telefono', 'ciudad', 'cedula', 'fecha', 'tieneci']
        
class CargarPuntosForm(forms.Form):
    fecha = forms.DateField(widget=forms.SelectDateWidget)
    marca = forms.CharField(max_length=100, required=False)
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), empty_label=None)
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label=None)
    subcategoria = forms.ModelChoiceField(queryset=Subcategoria.objects.all(), empty_label=None)