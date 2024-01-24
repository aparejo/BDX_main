from django import forms
from .models import Participante, Puntaje

class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nombre', 'apellido', 'telefono', 'ciudad', 'cedula', 'fecha', 'tieneci']
        
class PuntajeForm(forms.ModelForm):
    class Meta:
        model = Puntaje
        fields = ('fecha', 'marca', 'tiempo', 'participante', 'evento', 'categoria', 'subcategoria')