from django import forms
from .models import Participante, Puntaje, Evento, Categoria, Subcategoria
from django import forms
from django.forms.widgets import SelectDateWidget

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'apellido', 'telefono', 'ciudad', 'cedula', 'fecha', 'tieneci']
        
class CargarPuntosForm(forms.Form):
    fecha = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control'}))
    marca = forms.FloatField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    evento = forms.ModelChoiceField(queryset=Evento.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    categoria = forms.ModelChoiceField(queryset=Categoria.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))
    subcategoria = forms.ModelChoiceField(queryset=Subcategoria.objects.all(), empty_label=None, widget=forms.Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['evento'].label_from_instance = lambda obj: obj.nombre
        self.fields['categoria'].label_from_instance = lambda obj: obj.nombre
        self.fields['subcategoria'].label_from_instance = lambda obj: obj.nombre