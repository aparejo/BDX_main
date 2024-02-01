import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDX.settings')
django.setup()
import csv
from datetime import datetime
from reto.models import Participante
from BDX import settings

def cargar_participantes():
    with open('datos_participantes.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')  # Utiliza el delimitador ';'
        next(lector_csv)  # Saltar la primera fila si contiene encabezados

        for fila in lector_csv:
            nombre = fila[0]
            apellido = fila[1]
            telefono = fila[2]
            ciudad = fila[3]
            cedula = fila[4]
            fecha = datetime.strptime(fila[5], '%Y-%m-%d')
            tieneci = bool(fila[6])

            # Verificar si el participante ya está registrado
            if Participante.objects.filter(cedula=cedula).exists():
                continue  # Pasar al siguiente participante

            participante = Participante(
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                ciudad=ciudad,
                cedula=cedula,
                fecha=fecha,
                tieneci=tieneci,
            )
            participante.save()

cargar_participantes()