# Importamos librerías
import requests
from lxml import html
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import csv 
import re

#####  Definimos variables generales  ########

headers={
    "Accept": "*/*",
    "Content-Encoding": "gzip",
    "Cache-Control": "max-age=1206531",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
}

# Url Base

URL = "https://www.atrapalo.com/entradas/"

# Diccionario donde almacenamos las secciones o tipos de entradas
SECCIONES = {
            'teatro-y-danza' : 'Teatro y Danza',
            'musica': 'Música',
            'parques-tematicos': 'Parques temáticos', 
            'musicales': 'Musicales',
            'museos-y-exposiciones':'Museos y Exposiciones',
            'deportes':'Deportes',
            'circo': 'Circo',
            'cine': 'Cine',
            'feria':'Ferias'
            }

# Utilizaremos la versión 'temp'  de la variable SECCIONES durante las pruebas
SECCIONES = {'teatro-y-danza' : 'Teatro y Danza'}

#####  FUNCIONES  ########

def Sacar_espectaculos(url):
    
    respuesta = requests.get(url, headers=headers)
    soup = BeautifulSoup(respuesta.content, "html.parser")
    nuevos_espectaculos = soup.find_all(class_="card-result-container")    
    return(nuevos_espectaculos)

#####  PROG PPAL  ########

espectaculos = []
espectaculos_pantalla_anterior = []

# Primer Bucle para recorrer todas y cada una de las secciones de la página ( circo, musicales, etc)
for seccion in SECCIONES:
    cont = 1
    seguir_buscando = True
    
    # Recorremos todas y cada una de las pantallas de cada sección.Sólo hay 20 entradas por pantalla
    while seguir_buscando:
        url = URL + seccion + '/' + 'p-' + str(cont) + '/'
        cont += 1
        
         # Este código es temporal y sólo válido para el desarrollo de las pruebas, puesto que sólo leeremos 3 páginas por sección
        #if cont==3:
            #seguir_buscando = False
        
        espectaculos_pantalla = Sacar_espectaculos(url)
        # Imprimimos el resultado de cada llamada
        print(url,":", len(espectaculos_pantalla))
        
        if espectaculos_pantalla == espectaculos_pantalla_anterior:
            seguir_buscando = False            
        else:
            for espectaculo in espectaculos_pantalla:
                espectaculos.append(espectaculo)
            espectaculos_pantalla_anterior = espectaculos_pantalla
            
           
