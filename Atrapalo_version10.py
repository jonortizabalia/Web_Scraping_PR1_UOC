import requests
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl
import datetime
import random
import re
import csv
import os
import time   # v05 
import getpass #v05 Necesraio para detectar el user loggeado actualmente en el sistema


# ahora = datetime.datetime.now()
# ahora.year


######## Codigo PERSONAL###############
proxy_on = False

proxies_home = None
proxies_work = {
    "http": (removed) ,
    "https": (removed),
}

if proxy_on:
    proxies = proxies_work
else:
    proxies = proxies_home
########################################

headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

URL = "https://www.atrapalo.com/entradas/"

SECCIONES = {'teatro-y-danza' : 'Teatro y Danza', 
           'musica': 'Música', 
           'parques-tematicos': 'Parques temáticos', 
            'musicales': 'Musicales',
            'museos-y-exposiciones':'Museos y Exposiciones',
            'deportes':'Deportes',
            'circo': 'Circo',
            'cine': 'Cine',
            'ferias':'Ferias'}


#SECCIONES = {'teatro-y-danza' : 'Teatro y Danza'}
#SECCIONES = {'teatro-y-danza' : 'Teatro y Danza', 'circo' : 'Circo','musica': 'Música'}
SECCIONES = {'circo' : 'Circo'}

#atributos = ["Titulo","Categoria","Novedad","Ubicación","Localidad","Precio","Descuento", # -Añadida en v04
#                     "Fechas", "Fecha_inicio", "Fecha_fin","Duracion","Idioma","Publico",
#                     "Puntuación","Valoración","Opiniones"]

# v05  Añadidos nuevos atributos Captura, Web, Evento
atributos = ["Captura", "Web", "Evento", 
             "Titulo","Categoria","Novedad","Ubicación","Localidad","Precio","Descuento", 
             "Fechas", "Fecha_inicio", "Fecha_fin","Duracion","Idioma","Publico",
             "Puntuación","Valoración","Opiniones"]

origen = 'Atrapalo'    # Añadido en  v05

# path = "C:/Users/Usuario/Desktop/output.csv" # -Añadida en v04

fichero_csv = 'output.csv'
# v05. Permite obviar el usuario con el que se haya loggeado el usuario en el sistema
path = "C:/Users/" + getpass.getuser() + "/Desktop/" + fichero_csv  # Añadido v05

# Estas variables sirven para controlar el número de registros a descargar
modo_prueba = False
pantallazos = 2  #100 registros de pruebas (5 pantallazos x 20 registros)
