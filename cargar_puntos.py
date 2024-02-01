import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BDX.settings')
django.setup()
import csv
from datetime import datetime
from reto.models import Participante, Puntaje, Evento

def cargar_puntajes():
    with open('datos_puntajes.csv', 'r') as archivo_csv:
        lector_csv = csv.reader(archivo_csv, delimiter=';')  # Utiliza el delimitador ';'
        next(lector_csv)  # Saltar la primera fila si contiene encabezados

        for fila in lector_csv:
            cedula = fila[0]
            fecha = datetime.strptime(fila[1], '%Y-%m-%d')
            marca = int(fila[2])
            evento_nombre = fila[3]
            categoria_nombre = fila[4]
            subcategoria_nombre = fila[5]

            # Obtener el participante correspondiente a la cédula
            participante = Participante.objects.get(cedula=cedula)

            # Obtener el evento correspondiente al nombre
            evento = Evento.objects.get(nombre=evento_nombre)

            # Buscar la categoría y subcategoría correspondientes, si existen
            categoria = None
            subcategoria = None
            if categoria_nombre:
                categoria = evento.categoria_set.get(nombre=categoria_nombre)
            if subcategoria_nombre:
                subcategoria = categoria.subcategoria_set.get(nombre=subcategoria_nombre)

            puntaje = Puntaje(
                fecha=fecha,
                marca=marca,
                participante=participante,
                evento=evento,
                categoria=categoria,
                subcategoria=subcategoria,
            )
            puntaje.save()

cargar_puntajes()